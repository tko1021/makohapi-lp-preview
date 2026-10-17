"""特定継続的役務（パソコン教室）の解約時上限を検算する準備コード。

消費者庁 https://www.no-trouble.caa.go.jp/what/continuousservices/
2026-10-17再確認。法の適用・解除の有効性・役務開始・提供済み対価は
呼出元で確認する。このコードは日付からクーリング・オフを失効させず、
返金API、実台帳、個人データを扱わない。端数はDecimalで保持し、丸めない。
"""
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Ceiling:
    receivable_cap: Decimal
    refund_floor: Decimal


def cancellation_ceiling(*, total_yen: int, paid_yen: int,
                         delivered_yen: int, phase: str) -> Ceiling:
    """確認済みの金額と解除区分だけを受け取る。未確認値の既定値はない。

    phase: cooling_off / before_service / after_service
    receivable_capは上限であり、自動的にこの金額を請求する指示ではない。
    refund_floorは上限まで受け取る場合の最小返金額。実際に低い請求額を
    選ぶ場合、その分だけ返金額は増える。提供済み対価は回数から推定しない。
    """
    values = (total_yen, paid_yen, delivered_yen)
    if any(type(value) is not int for value in values):
        raise TypeError('確認済みの整数円が必要です。未確認、真偽値、小数は受け取りません')
    if total_yen <= 0 or not 0 <= paid_yen <= total_yen or not 0 <= delivered_yen <= total_yen:
        raise ValueError('金額が契約総額の範囲外です。過入金等は個別確認してください')
    if phase not in ('cooling_off', 'before_service', 'after_service'):
        raise ValueError('確認済みの解除区分が必要です')
    if phase == 'before_service' and delivered_yen != 0:
        raise ValueError('開始前という区分と提供済み対価が矛盾しています')

    total, paid, delivered = (Decimal(value) for value in values)
    if phase == 'cooling_off':
        cap = Decimal(0)
    elif phase == 'before_service':
        cap = min(total, Decimal(15000))
    else:
        remaining = total - delivered
        damages_cap = min(Decimal(50000), remaining * Decimal('0.20'))
        cap = delivered + damages_cap
    return Ceiling(receivable_cap=cap, refund_floor=max(Decimal(0), paid - cap))
