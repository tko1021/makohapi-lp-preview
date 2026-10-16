# まこハピAIスクール LP（公開ページの正本）

このリポジトリは **まこハピAIスクールのLP（ランディングページ）そのもの**です。
`main` に push すると GitHub Pages が自動で更新され、約1〜2分で
https://tko1021.github.io/makohapi-lp-preview/ に反映されます。

**ここが唯一の正本です。** 別リポジトリ ai-school の `lp/index_design.html` は古い原稿で、
公開には効きません（2026-10-15 本人決定）。

## ファイル

| ファイル | 役割 |
|---|---|
| `index.html` | 短縮LP |
| `complete.html` | 講座の完全版 |
| `design.css` | 見た目（色・余白・フォント） |
| `tokushoho.html` / `privacy.html` / `terms.html` | 法務表示の確認用原稿 |
| `gaiyo_shomen.html` / `contract_sample.html` | 法定書面の確認用原稿・見本 |
| `application-flow.html` | 申込準備の流れと未完了項目 |
| `measurement.js` | 外部送信なしの計測イベント準備 |
| `check.py` | 公開前の機械検査（下記）。標準ライブラリだけで動く |
| `.nojekyll` | GitHub Pages にそのまま配信させる印。消さない |

セクションの id：`philosophy`（考え方）／`cases`（実例）／`curriculum`（カリキュラム）／
`support`（サポート）／`instructor`（講師）／`requirements`（募集要項）／`entry`（申込）。
「〇〇の節を直して」と言われたら、この id を目印に探す。

## 直し方（スマホのClaudeアプリから頼まれたとき、この順番で）

**既定は「プレビューまで」。公開（main への反映）は、本人が「公開して」と言ったときだけ。**
（2026-10-15 本人決定「反映までいかなくても、確認とプレビューできればいい」）

1. 頼まれた箇所だけを `index.html`（または `design.css`）で直す。頼まれていない箇所は触らない。
2. `python3 check.py` を走らせる。**CHECK PASSED でなければ push しない。** NG の行をそのまま本人に見せる。
3. 変えた箇所を「変更前 → 変更後」で本人に見せる（長い説明は要らない。文言の差分だけ）。
4. **作業用ブランチ**に commit して push する（main には push しない）：
   ```bash
   git add index.html design.css
   git commit -m "lp: <何を変えたか一言>"
   git push -u origin HEAD
   ```
5. push したコミット番号でプレビューURLを作り、**押せるリンクとして**本人に渡す：
   ```bash
   echo "https://htmlpreview.github.io/?https://github.com/tko1021/makohapi-lp-preview/blob/$(git rev-parse HEAD)/index.html"
   ```
   ブランチ名ではなくコミット番号を使う（キャッシュで古い版が出るのと、ブランチ名の「/」で壊れるのを防ぐ）。
   「このリンクをスマホで開くと、公開前の見た目を確認できます。公開してよければ『公開して』と送ってください」と添える。
6. 本人が「公開して」と言ったときだけ、同じ内容を main へ push する：
   ```bash
   git push origin HEAD:main
   ```
   push 後に「約1〜2分で https://tko1021.github.io/makohapi-lp-preview/ に反映されます」と伝える。

## 守ること（check.py が機械で止めるもの）

- **入力欄（input/textarea/select/iframe）を置かない**。このページは個人情報を受け取らない。
- **外部リンクを足さない**。リンクはページ内と、このリポジトリ内の確認用ページだけ。
  外部リンク（申込フォーム・LINE・決済など）を足すのは、本人が「正式募集に切り替える」と決めたとき。
  そのときは check.py の条件も一緒に本人決定として変える。
- `<meta name="robots" content="noindex,nofollow">` を消さない。
- 「申込受付は開始していません」の文言を消さない（同上）。
- 鍵・パスワード・個人名・顧客データをこのリポジトリに置かない（**公開リポジトリ**です）。

## 判断に迷ったら

- 文言の表現を変える・誤字を直す・順番を入れ替える・色や余白を変える → **可逆。聞かずにやる。**
- 節を丸ごと消す・料金や日程の数字を変える・上の「守ること」に触れる → **一度だけ確認してから。**
- 外部の事実（制度・法令・料金）を書き足すときは、記憶で書かず出典を本人に確認する。
