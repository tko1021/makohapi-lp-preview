"""実顧客を使わず、手計算した金額と不正入力を検証する。"""
from decimal import Decimal
import unittest

from tools.refund_check import cancellation_ceiling


class RefundCheckTests(unittest.TestCase):
    def test_cooling_off_refunds_all_even_after_delivery(self):
        value = cancellation_ceiling(total_yen=110000, paid_yen=110000,
                                     delivered_yen=55000, phase='cooling_off')
        self.assertEqual(value.receivable_cap, Decimal(0))
        self.assertEqual(value.refund_floor, Decimal(110000))

    def test_before_start_cap_and_refund(self):
        value = cancellation_ceiling(total_yen=110000, paid_yen=110000,
                                     delivered_yen=0, phase='before_service')
        self.assertEqual(value.receivable_cap, Decimal(15000))
        self.assertEqual(value.refund_floor, Decimal(95000))

    def test_after_start_with_half_value_delivered(self):
        # 残額55,000円、損害上限11,000円、受取上限66,000円。
        value = cancellation_ceiling(total_yen=110000, paid_yen=110000,
                                     delivered_yen=55000, phase='after_service')
        self.assertEqual(value.receivable_cap, Decimal(66000))
        self.assertEqual(value.refund_floor, Decimal(44000))

    def test_higher_hypothetical_contract_uses_50000_cap(self):
        # 本講座の値札ではない架空の境界試験。残額80万円の20%より5万円が低い。
        value = cancellation_ceiling(total_yen=1000000, paid_yen=1000000,
                                     delivered_yen=200000, phase='after_service')
        self.assertEqual(value.receivable_cap, Decimal(250000))
        self.assertEqual(value.refund_floor, Decimal(750000))

    def test_fractional_yen_remains_exact_without_rounding(self):
        value = cancellation_ceiling(total_yen=110000, paid_yen=110000,
                                     delivered_yen=40001, phase='after_service')
        self.assertEqual(value.receivable_cap, Decimal('54000.80'))
        self.assertEqual(value.refund_floor, Decimal('55999.20'))

    def test_paid_less_than_cap_does_not_produce_negative_refund(self):
        value = cancellation_ceiling(total_yen=110000, paid_yen=10000,
                                     delivered_yen=0, phase='before_service')
        self.assertEqual(value.refund_floor, Decimal(0))

    def test_fully_delivered_has_no_unused_value(self):
        value = cancellation_ceiling(total_yen=110000, paid_yen=110000,
                                     delivered_yen=110000, phase='after_service')
        self.assertEqual(value.receivable_cap, Decimal(110000))
        self.assertEqual(value.refund_floor, Decimal(0))

    def test_unknown_or_invalid_amounts_are_rejected(self):
        for name in ('total_yen', 'paid_yen', 'delivered_yen'):
            for invalid in (None, True, '110000', 110000.0, Decimal('NaN')):
                with self.subTest(name=name, invalid=invalid), self.assertRaises(TypeError):
                    args = dict(total_yen=110000, paid_yen=110000,
                                delivered_yen=0, phase='before_service')
                    args[name] = invalid
                    cancellation_ceiling(**args)

    def test_out_of_range_amounts_are_rejected(self):
        for total, paid, delivered in ((0, 0, 0), (110000, -1, 0),
                                       (110000, 110001, 0), (110000, 0, -1),
                                       (110000, 0, 110001)):
            with self.subTest(values=(total, paid, delivered)), self.assertRaises(ValueError):
                cancellation_ceiling(total_yen=total, paid_yen=paid,
                                     delivered_yen=delivered, phase='after_service')

    def test_unknown_phase_is_not_treated_as_cooling_off_expired(self):
        with self.assertRaises(ValueError):
            cancellation_ceiling(total_yen=110000, paid_yen=110000,
                                 delivered_yen=0, phase='unknown')

    def test_phase_and_delivered_amount_must_agree(self):
        with self.assertRaises(ValueError):
            cancellation_ceiling(total_yen=110000, paid_yen=110000,
                                 delivered_yen=1, phase='before_service')


if __name__ == '__main__':
    unittest.main()
