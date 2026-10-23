# lesson03 講義スライド

`lesson03_slides.md` がMarp形式の編集用ファイルです。全44枚で、lesson03のNotebookと併用します。slides_02と同じ16:9のサイズ・配色・書体・実習ページの形式です。

- `lesson03_slides.html`：ブラウザーで開く講義用スライド。左右の矢印キーで移動できます。
- `lesson03_slides.pdf`：配布・閲覧用。
- `assets/`：教材データから描画した図と、評価表の計算値。

HTMLと`assets`は、同じ位置関係を保って配布してください。PDFは単独で使えます。

## 講義の進め方

相関、ペンギンの単回帰、アイスクリームの単回帰・重回帰、予測の評価の順に進みます。淡い緑の「Notebookで実習」でNotebookへ移り、実行後にスライドへ戻って結果を共有します。

| 実習スライド | Notebookの見出し | 確認すること |
| --- | --- | --- |
| 8 | 2. 散布図と相関係数 | 関係の向き・強さと、相関だけでは捉えにくい曲線 |
| 15 | 3. ペンギンの翼の長さと体重で単回帰を試す | 傾き・切片・入力を変えた予測 |
| 19 | 4. アイスクリームのデータを読む／5. 学習期間とテスト期間を分ける | 1行の意味と、学習96件・テスト24件の分割 |
| 23 | 6. 気象データと購入額の関係を見る／7. 気温から購入額を予測する（単回帰） | 相関と回帰式、範囲内での予測 |
| 27 | 8. 複数の気象変数を使う（重回帰） | 係数の意味・単位と、説明変数どうしの相関 |
| 32 | 9. 学習に使わなかった期間で評価する | MAE・RMSEと、4つの方法の比較 |
| 35 | 10. 予測と実測を図で比べる／残差から予測のずれを読む | 過大予測・過小予測と、ずれが大きい時期 |
| 42 | まとめとレポート／演習A〜C | レンタサイクルの演習と提出前の確認 |

スライド38〜40は演習A〜Cの説明です。本文で使ったアイスクリームとは別に、運用している日の18時のレンタサイクル貸出件数を扱います。演習Bでは気温の入力値を変更します。完全な実行コードとレポート本文のテンプレートはNotebookにあります。

学習と評価の図は、初期設定を実行した例です。受講者が入力や設定を変えた場合は、自分の結果をレポートに使います。スライド中の短いコードは要点のみで、本文の事前セルを実行して使うものです。演習A〜Cのコードセルは、それぞれ単独で実行できます。

講師向けの補足と出典は、MarkdownのHTMLコメントにも記載しています。Notebook巻末の発展演習は、基本講義のスライドには含めていません。

## 編集と書き出し

VS Codeの「Marp for VS Code」でMarkdownを開くとプレビューできます。Node.jsとMarp CLIを使う場合は、リポジトリのルートで次を実行します。

```sh
npx @marp-team/marp-cli slides_03/lesson03_slides.md --html -o slides_03/lesson03_slides.html
npx @marp-team/marp-cli slides_03/lesson03_slides.md --html --pdf --allow-local-files -o slides_03/lesson03_slides.pdf
```

PDFの書き出しにはChromeなどの対応ブラウザーが必要です。HTMLタグを使用しているため、`--html`を付けています。

## 図と数値の出典

`../notebook/lesson03_regression_basic_template.ipynb` の本文コードを、同梱データで再実行して作成しています。Notebookファイルの保存済み出力には依存しません。

- `correlations.png`：Notebookと同じ乱数シード42の人工データ。スライド用に図の縦横比を調整。
- `penguin_regression.png`：Palmer PenguinsのAdelie151羽。翼の長さ・体重の欠損を除外。
- `ice_correlations.png`：学習期間の気温・湿度と購入額。Notebookの5変数の散布図から2変数を選び、読みやすい大きさで再描画。
- `ice_single.png`：学習期間の気温を用いた単回帰。
- `ice_predictions.png`、`ice_residuals.png`：2011〜2012年のテスト期間の予測と残差。
- `metrics.json`：同じ実行で計算した4つの方法のMAE・RMSE。スライド31は小数第1位に丸めて掲載。
- スライド28〜29の500円の例は、誤差の計算を説明するための例示データ。

ペンギンは[Palmer Penguins](https://allisonhorst.github.io/palmerpenguins/)（CC0）、レンタサイクルは[Seoul Bike Sharing Demand](https://doi.org/10.24432/C5F62R)（CC BY 4.0）です。アイスクリームは既存教材から引き継いだデータで、地域・購入額の集計対象・一次出典は不明です。詳しい列・期間・取得条件は `../notebook/datasets/README.md` を参照してください。

Notebookのコードやデータを変更した場合は、対応する画像・評価表も更新してからHTML・PDFを書き出してください。
