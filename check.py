#!/usr/bin/env python3
"""公開LP（index.html / design.css）の機械検査。標準ライブラリだけで動く。

使い方:  python3 check.py          → 全部通れば「CHECK PASSED」・終了コード0
                                       1つでも落ちれば NG の行を出して終了コード1

見るもの（公開前の約束。2026-09-23 の公開時に決めた条件と同じ）
  1. 入力欄が無い（input / textarea / select / iframe を置かない＝個人情報を受け取らない）
  2. form は method="dialog" の1つだけ（送信先サーバーを持たない）
  3. リンク先はページ内（#…）か design.css だけ（外部へ飛ばさない）
  4. <meta name="robots" content="noindex,nofollow"> が残っている
  5. 「申込受付は開始していません」の文言が残っている（正式募集に切り替えるときは本人の決定で外す）
  6. 見出し h1 が1つだけ
  7. design.css が index.html から参照されている
"""
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "index.html"
CSS = ROOT / "design.css"


class Audit(HTMLParser):
    def __init__(self):
        super().__init__()
        self.inputs, self.forms, self.links, self.h1, self.robots = [], [], [], 0, None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("input", "textarea", "select", "iframe"):
            self.inputs.append((tag, self.getpos()[0]))
        if tag == "form":
            self.forms.append((a, self.getpos()[0]))
        if tag == "h1":
            self.h1 += 1
        if tag == "meta" and a.get("name") == "robots":
            self.robots = a.get("content", "")
        for name in ("href", "src", "action"):
            if name in a:
                self.links.append((a[name], self.getpos()[0]))


def main() -> int:
    ng = []
    if not HTML.exists():
        print("NG index.html が無い"); return 1
    if not CSS.exists():
        ng.append("design.css が無い")
    html = HTML.read_text(encoding="utf-8-sig")
    au = Audit(); au.feed(html)

    if au.inputs:
        ng.append(f"入力欄がある: {au.inputs}")
    if [f for f, _ in au.forms] != [{"method": "dialog"}]:
        ng.append(f"form が method=dialog の1つだけでない: {au.forms}")
    bad = [(l, n) for l, n in au.links if not (l.startswith("#") or l == "design.css")]
    if bad:
        ng.append(f"ページ外へのリンクがある: {bad}")
    if au.robots != "noindex,nofollow":
        ng.append(f"robots が noindex,nofollow でない: {au.robots!r}")
    if "申込受付は開始していません" not in html:
        ng.append("「申込受付は開始していません」の文言が消えている（正式募集なら本人決定を記録してから）")
    if au.h1 != 1:
        ng.append(f"h1 が {au.h1} 個（1個のはず）")
    if "design.css" not in [l for l, _ in au.links]:
        ng.append("design.css が参照されていない")

    for line in ng:
        print("NG", line)
    if ng:
        print(f"CHECK FAILED ({len(ng)}件)")
        return 1
    print(f"CHECK PASSED  index.html {HTML.stat().st_size} bytes / design.css {CSS.stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
