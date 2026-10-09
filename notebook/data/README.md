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
