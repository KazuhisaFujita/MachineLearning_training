# 月平均気温（2025年）

`monthly_mean_temperature_2025.csv` は、広島・津山・金沢の2025年1〜12月の月平均気温をまとめたlesson02用の教材データです。

- 列: `月`（1〜12）、`広島`、`津山`、`金沢`
- 気温の単位: ℃。気象庁の「月ごとの値」の「気温 → 日平均 → 平均」を転記しています。最高気温と最低気温の平均ではありません。
- 各地点の観測値であり、市全域の平均や複数年の平年値ではありません。
- 全36値に欠測や品質に関する付記記号はありません。
- 文字コード: UTF-8（BOM付き）。pandasの `pd.read_csv('data/monthly_mean_temperature_2025.csv')` で読み込めます（notebookディレクトリから実行）。
- 確認日: 2026年10月9日。気象庁のデータは後日修正される場合があります。

出典: 気象庁「過去の気象データ検索」、2025年、月ごとの値、詳細（気温・蒸気圧・湿度）。

- [広島（地点番号47765）](https://www.data.jma.go.jp/stats/etrn/view/monthly_s1.php?prec_no=67&block_no=47765&year=2025&month=&day=&view=a2)
- [津山（地点番号47756）](https://www.data.jma.go.jp/stats/etrn/view/monthly_s1.php?prec_no=66&block_no=47756&year=2025&month=&day=&view=a2)
- [金沢（地点番号47605）](https://www.data.jma.go.jp/stats/etrn/view/monthly_s1.php?prec_no=56&block_no=47605&year=2025&month=&day=&view=a2)


# アイスクリームの平均購入額と気象データ

`ice.csv` は、既存教材 `regression/ice.csv` を内容を変更せずコピーしたlesson03用データです。`regression/ice.ipynb` の散布図・相関・単回帰の題材を引き継いでいます。

- 期間・件数: 2003年1月〜2012年12月、1行が1か月、計120行。
- 列: `年`、`月`、`アイスクリームの平均購入額`、`日最高気温の平均(℃)`、`降水量の合計(mm)`、`平均湿度(％)`、`日最高気温25℃以上日数(日)`。
- 購入額の単位は元Notebookの表記に従い円としています。気温は日最高気温の月平均です。
- 元教材には地域、購入額の集計対象、一次出典の記載がありません。店舗の売上や個人の購入額と断定せず、既存教材の分析用データとして扱ってください。
- 文字コード: UTF-8。`notebook` ディレクトリから `pd.read_csv('data/ice.csv')` で読み込めます。
- lesson03では2003〜2010年を学習期間、2011〜2012年をテスト期間に使います。


# ペンギンの翼の長さと体重

`penguins.csv` はPalmer Penguinsの簡略版データを配布元のCSVから変更せず保存した、lesson03の単回帰導入用データです。

- 全344行・8列。1行が1羽のペンギンで、Adelie・Chinstrap・Gentooの3種を含みます。
- lesson03ではAdelieを選び、`flipper_length_mm`（翼の長さ、mm）と`body_mass_g`（体重、g）の欠損行を除いた151羽を使用します。CSV自体は種の抽出・欠損行の削除をしていません。
- 観測: Kristen Gorman氏、Palmer Station Antarctica LTER。観測年は2007〜2009年。
- ライセンス: CC0。文字コード: UTF-8。取得日: 2026年10月17日。
- [公式ページ・データの説明](https://allisonhorst.github.io/palmerpenguins/)
- [取得したCSV](https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/inst/extdata/penguins.csv)
- 元論文: Gorman KB, Williams TD, Fraser WR (2014). Ecological sexual dimorphism and environmental variability within a community of Antarctic penguins (genus Pygoscelis). [PLOS ONE, 9(3), e90081](https://doi.org/10.1371/journal.pone.0090081).
