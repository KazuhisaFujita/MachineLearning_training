# lesson05 講義スライド

`lesson05_slides.md` がMarp形式の編集用ファイルです。全46枚で、lesson05のNotebookと併用します。slides_02〜04と同じ16:9のサイズ・配色・書体・実習ページの形式です。

- `lesson05_slides.html`：ブラウザーで開く講義用スライド。左右の矢印キーで移動できます。
- `lesson05_slides.pdf`：配布・閲覧用。
- `assets/`：教材データから描画した図と、評価表の計算値。

HTMLと`assets`は、同じディレクトリ構成を保って配布してください。PDFは単独で使えます。

## 前回の講義との接続

lesson04（分類）を受講済みで、リポジトリ直下の `08_classification.pdf`・`09_classification.pdf` に引き続いて、講義資料1「ニューラルネットワークの歴史と手法1（パーセプトロンまで）」と講義資料2「ニューラルネットワークの歴史と手法2（HubelとWieselからLeNetまで）」を配布できる状態を想定しています。前回の「種類を予測する」から、今回は**予測のつくり方を学習する**へ進みます。

- スライド3で、資料の式とNotebookのコードを1対1で対応付けます（線形閾値素子→`nn.Linear`（バイアス$b$も含む）、活性化関数→`nn.ReLU`、誤差関数→`MSELoss`/`CrossEntropyLoss`、勾配降下と学習率→`optimizer`/`lr`（Adamは勾配降下の改良版）、誤差逆伝播→`loss.backward()`、batch learning→1エポック＝学習用全件で1回更新）。
- スライド7は資料1の $a=\sum_i w_i x_i$、スライド8・9は資料2の活性化関数と「多層化すると直線ではなくなる」に対応します。スライド11の4ステップが資料2の $w \leftarrow w-\eta\nabla E(w)$ そのものです。
- lesson04スライド17で出した「**学習用によく合うことと、未知データで当たることが同じとは限らない**」を、今回は検証用データとエポック選び（スライド5・20・34・43）の中心に据えます。
- スライド38の仮の花（花弁の長さ5.0cm・幅1.7cm）は、lesson04で「新しい花」として扱った同じ位置です。今回はテスト用30輪の中にも同じ座標の花（実際の種類はversicolor）があり、誤分類の2輪の1つになっています。ただしlesson04は2クラス・今回は3クラスで、データの分け方も異なるため、**lesson04の正解率0.900などとは比較しません**（スライド36にも明記しています）。
- lesson03で使ったアイスクリームデータですが、今回は検証期間を分けたため**学習期間がlesson03と異なります**（学習72か月／検証24か月／テスト24か月）。

## 講義の進め方

資料との対応、LinearとReLU、学習の4ステップ、アイス（回帰）、Iris（分類）、共通点の整理の順に進みます。12でエポックとbatch learning、20で「検証RMSEが最小のエポック（481）は最後のエポック（600）ではない」、34で「検証損失が最小のエポック（22）は正解率が最大のエポック（17）でもない」、35で「正解率が頭打ちでも損失は動く」を確認します。淡い緑の「Notebookで実習」でノートブックへ移り、実行後にスライドへ戻って結果を共有します。

| 実習スライド | Notebookの見出し | 確認すること |
| --- | --- | --- |
| 13 | 1. 共通の準備／2. 回帰 | 3分割の件数と散布図 |
| 26 | 2.4 テスト期間で予測できるか確かめる | 3つの方法のMAE・RMSE |
| 40 | 3.3 テスト用の花を分類する | 正解率と誤分類の位置 |
| 44 | 4. 共通点／振り返りとレポート | 回帰と分類の表の埋め方 |

スライドの数値は、Notebookを初期設定（乱数シード42）で実行した結果です。テストの評価は、**検証用で選んだ重み**（回帰は検証RMSEでepoch 481、分類は検証損失でepoch 22）を読み戻したときの値であり、テスト用はエポックの確認に使っていません。受講者がエポック数・隠れ層・学習率を変えた場合は、自分の結果をレポートに使います。

「NNが常に優れる」「過学習が起きている」とは断定していません。回帰のテストでは3方法のうちNNの誤差が最も小さいですが、これは気温1つ・同じ学習期間という条件です。分類の検証損失はepoch 22の0.155を底に、その後は0.155〜0.250の間を動きますが、検証正解率は下がっていません。講師向けの補足と留保は、MarkdownのHTMLコメントにも記載しています。

## 編集と書き出し

VS Codeの「Marp for VS Code」でMarkdownを開くとプレビューできます。Node.jsとMarp CLIを使う場合は、リポジトリのルートで次を実行します。

```sh
npx @marp-team/marp-cli slides_05/lesson05_slides.md --html -o slides_05/lesson05_slides.html
npx @marp-team/marp-cli slides_05/lesson05_slides.md --html --pdf --allow-local-files -o slides_05/lesson05_slides.pdf
```

Node.jsがない環境では、Docker（Chromium同梱の公式イメージ）でも書き出せます。

```sh
docker run --rm -v "$PWD:/work" -w /work marpteam/marp-cli --html slides_05/lesson05_slides.md -o slides_05/lesson05_slides.html
docker run --rm -v "$PWD:/work" -w /work marpteam/marp-cli --html --pdf --allow-local-files slides_05/lesson05_slides.md -o slides_05/lesson05_slides.pdf
```

PDFの書き出しにはChromeなどの対応ブラウザーが必要です（Docker版はイメージ内のChromiumを使用）。HTMLタグと数式 `$...$` を使っているため、`--html` を付けています。数式はMathJax（CDN）で描画されるため、書き出し時にネットワークへ接続します。Docker版はコンテナ内のNoto Sans JPで描画され、macOSのChromeで書き出した場合とフォント・改行位置がわずかに変わります。

## 図と数値の出典

`slides_05/assets/generate_slides_assets.py` が、`notebook/lesson05_neural_network_basic_template.ipynb` の**コードセルを上から順にexec**し、図が出るセルの直後にPNGを保存します。Notebookファイルの保存済み出力には依存せず、軸範囲・色・乱数シード・エポック数までNotebookと同一です。同じ実行から `metrics.json` も出力します。実行はリポジトリのルートで次を行います（Matplotlib・PyTorchが必要）。

```sh
.venv/bin/python slides_05/assets/generate_slides_assets.py
```

Notebook側で、アイスデータのパスが `data/ice.csv`・`data/README.md`（フォルダ名の変更の名残で実在しない）になっていたため、`datasets/ice.csv`・`datasets/README.md` に修正しています。修正しないとNotebookは実行できません。

生成環境は Python 3.13.5 / PyTorch 2.10.0 / scikit-learn 1.7.2 / Matplotlib 3.10.7 です。Notebookの保存済み出力（PyTorch 2.14.1・macOS）と、再実行で得た主要な数値は**すべて一致**しました（回帰: 検証RMSE最小epoch 481・84.8円、テストRMSE 85.6円、25℃の予測680.4円／分類: 検証損失最小epoch 22・0.155、テスト正解率93.3%＝28/30輪、仮の花の確率0.709・0.291・0.000016）。ただしPyTorchのバージョン違いで数値は変わることがあり、これはNotebook冒頭の注意と同じです。

- `ice_scatter.png`：学習用72か月・検証用24か月の散布図（スライド14）。
- `reg_curves.png`：epoch 0・20・100・600の予測曲線（スライド18）。
- `reg_learning_curve.png`：毎エポックの学習用・検証用RMSEと、検証最小のエポック481（スライド19）。
- `reg_test.png`：テスト24か月の予測=実測の散布図と月次推移（スライド24）。
- `iris_scatter.png`：学習用90輪の散布図（スライド27）。
- `cls_boundaries.png`：epoch 0・10・50・200の識別領域と検証正解率、誤分類の×（スライド31）。
- `cls_learning_curve.png`：正解率と交差エントロピー損失の推移、検証損失最小のエポック22（スライド33）。
- `cls_test.png`：epoch 22の識別領域と、テスト用30輪・誤分類2輪（スライド37）。
- `relu.png`：ReLUの形。資料1のステップ関数と資料2のシグモイドを同じ図に並べた**説明用の関数図**（スライド8）。
- `network_architecture.png`：回帰（1→16→16→1）と分類（2→16→16→3）の**模式図**。隠れ層の16個も実際に描いています（スライド10）。
- `reg_vs_linear.png`：学習済みNN（epoch 481）の予測曲線と単回帰の直線の比較（スライド22）。**直線はlesson03本文のモデルではなく、lesson05の学習用72か月に同じ形 ŷ=wx+b でフィットしたもの**（ŷ = 34.2x − 111.3）で、Notebook本文にはない計算です。NNの曲線はNotebookと同じ実行から得ています。
- `cls_prob_new_flower.png`：仮の花（長さ5.0cm・幅1.7cm）のクラス確率（スライド38）。setosaは 1.6×10⁻⁵ で、0ではありません。
- `metrics.json`：上の図と同じ実行から計算した値。RMSE・損失・正解率のエポック別の一覧、選択エポック、テストのMAE・RMSE、25℃の予測、テスト各月の実測と予測、単回帰の係数、学習用を気温で分けた購入額の分布、検証損失・検証正解率の最大値と変動範囲、学習前（epoch 0）の予測内訳、識別領域のクラス面積比、テストの誤分類、仮の花の確率、実行環境のバージョンを収録します。スライド15・20・21・22・23・24・32・34・35・36・38・41の数値は、このファイルの値と一致します（スライド内のHTMLコメントに、どのキーの出典かを記載しています）。

アイスは `notebook/datasets/ice.csv`（既存教材から引き継いだデータで、地域・購入額の集計対象・一次出典は不明）。Irisはscikit-learnの`load_iris()`に含まれる実測データ（R. A. Fisher, 1936）で、花弁の長さ・幅の2列と3種類のラベルを使います。列・期間・取得条件の詳細は `notebook/datasets/README.md` を参照してください。

Notebookのコードやデータを変更した場合は、`generate_slides_assets.py`（図と`metrics.json`）を再実行してから、HTML・PDFを書き出してください。

図中の日本語について: Notebookは `font.family = sans-serif` にmacOS向けフォント（Hiragino Sansなど）を並べますが、matplotlibは `sans-serif` を解決するときに最も合う1フォントしか選ばないため、`font.sans-serif` の2番目以降は文字単位のフォールバックに使われません。日本語グリフを持たないフォントが選ばれ、図中の日本語が豆腐（□）になります。そこで `generate_slides_assets.py` は各セルの実行後に `font.family` へ**実在するフォント名**を直接並べます（見つかった日本語フォント → DejaVu Sans → Droid Sans Fallback）。macOSでは先頭がHiragino SansのままなのでNotebookと同じ描画になり、日本語フォントが無いLinux環境では DejaVu Sans（欧文）＋Droid Sans Fallback（日本語）で描画されます。PNG保存時はグリフ欠落の警告をエラーとして扱うため、豆腐が出る環境では生成が失敗して分かります。
