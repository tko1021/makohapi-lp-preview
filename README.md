# まこハピAIスクール LP

公開ページ：https://tko1021.github.io/makohapi-lp-preview/

`main` に push すると GitHub Pages が自動更新します（約1〜2分）。
編集のルールは `CLAUDE.md`、公開前の機械検査は `python3 check.py`。

## ページ構成

- `index.html`：短縮LP
- `complete.html`：講座の完全版
- `tokushoho.html`：特定商取引法に基づく表記（確認用）
- `privacy.html`：個人情報の取扱い（確認用）
- `terms.html`：受講規約（確認用）
- `gaiyo_shomen.html`：概要書面（確認用）
- `contract_sample.html`：契約書面見本
- `application-flow.html`：申込・書面交付・決済の準備状況
- `monitor_consent.html`：事例掲載同意書（確認用案・送信不可）
- `measurement.js`：外部送信を行わない計測イベントの準備コード
- `tools/refund_check.py`：解約時の上限額の検算用。実返金・法適用判定には未接続
- `tests/test_refund_check.py`：架空の金額による検算（`python -m unittest discover -s tests`）
- `reception_plan.json`：説明会受付・電子交付・計測の接続準備案。実フォーム・自動送信には未接続

無料説明会は2026年10月28日（水）20:00、講座は2026年11月19日～2027年2月18日、全12回です。
無料説明会の申込締切：2026年10月26日（月）23:59（2026年10月17日本人回答）。
申込フォーム、決済、電子交付、本番計測は未接続・未試験です。`noindex`と「申込受付前」を外してはいけません。

スマホのClaudeアプリから直す手順（ワンクリック単位）は、非公開リポジトリ ai-school の
`docs/スマホからLPを直す手順.md` にあります。
