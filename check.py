#!/usr/bin/env python3
"""短縮LP・完全版・法務確認用ページの機械検査。

使い方:  python3 check.py          → 全部通れば「CHECK PASSED」・終了コード0
                                       1つでも落ちれば NG の行を出して終了コード1

見るもの（公開前の約束。2026-09-23 の公開時に決めた条件と同じ）
  1. 入力欄が無い（input / textarea / select / iframe を置かない＝個人情報を受け取らない）
  2. LPのformはmethod="dialog"の1つだけ、法務ページにはformが無い
  3. リンク先はページ内・このリポジトリ内の確認用ページだけ
  4. <meta name="robots" content="noindex,nofollow"> が残っている
  5. 「申込受付は開始していません」の文言が残っている（正式募集に切り替えるときは本人の決定で外す）
  6. 見出し h1 が1つだけ
  7. design.css が両HTMLから参照されている
"""
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LP_FILES = (ROOT / "index.html", ROOT / "complete.html")
LEGAL_FILES = tuple(ROOT / name for name in (
    "tokushoho.html", "privacy.html", "terms.html", "gaiyo_shomen.html",
    "contract_sample.html", "application-flow.html",
))
HTML_FILES = LP_FILES + LEGAL_FILES
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
    if not CSS.exists():
        ng.append("design.css が無い")
    sizes = []
    allowed_files = {path.name for path in HTML_FILES} | {"design.css", "measurement.js"}
    for html_path in HTML_FILES:
        if not html_path.exists():
            ng.append(f"{html_path.name} が無い")
            continue
        html = html_path.read_text(encoding="utf-8-sig")
        sizes.append(f"{html_path.name} {html_path.stat().st_size} bytes")
        au = Audit(); au.feed(html)

        if au.inputs:
            ng.append(f"{html_path.name}: 入力欄がある: {au.inputs}")
        if html_path in LP_FILES and [f for f, _ in au.forms] != [{"method": "dialog"}]:
            ng.append(f"{html_path.name}: form が method=dialog の1つだけでない: {au.forms}")
        if html_path in LEGAL_FILES and au.forms:
            ng.append(f"{html_path.name}: 確認用法務ページにformがある: {au.forms}")
        bad = [(link, line) for link, line in au.links if not (link.startswith("#") or link in allowed_files)]
        if bad:
            ng.append(f"{html_path.name}: 許可していないリンクがある: {bad}")
        if au.robots != "noindex,nofollow":
            ng.append(f"{html_path.name}: robots が noindex,nofollow でない: {au.robots!r}")
        if "申込受付は開始していません" not in html:
            ng.append(f"{html_path.name}: 「申込受付は開始していません」の文言が消えている")
        if au.h1 != 1:
            ng.append(f"{html_path.name}: h1 が {au.h1} 個（1個のはず）")
        if "design.css" not in [link for link, _ in au.links]:
            ng.append(f"{html_path.name}: design.css が参照されていない")

    corpus = "\n".join(path.read_text(encoding="utf-8-sig") for path in HTML_FILES if path.exists())
    required = {
        "価格110,000円": "110,000",
        "開講日2026年11月19日": "2026年11月19日",
        "最大10名": "最大10名",
        "顔出し任意": "顔出しは任意",
        "クーリング・オフ8日": "8日以内",
        "開始前解約上限15,000円": "15,000円",
    }
    for label, text in required.items():
        if text not in corpus:
            ng.append(f"必須表示が無い: {label}")
    forbidden = ("100,000円", "2026年11月1日", "2026年10月28日", "2026年10月23日")
    for text in forbidden:
        if text in corpus:
            ng.append(f"旧条件が残っている: {text}")

    for line in ng:
        print("NG", line)
    if ng:
        print(f"CHECK FAILED ({len(ng)}件)")
        return 1
    print(f"CHECK PASSED  {' / '.join(sizes)} / design.css {CSS.stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
