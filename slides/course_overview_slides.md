---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  section {
    font-family: "Hiragino Sans", "Noto Sans JP", sans-serif;
    background: linear-gradient(135deg, #f7f4ea 0%, #fffdf8 52%, #eef6f1 100%);
    color: #1d2a2a;
    padding: 46px;
  }
  h1, h2, h3 {
    color: #143a36;
  }
  h1 {
    font-size: 1.8em;
    border-bottom: 4px solid #d98f3d;
    padding-bottom: 0.18em;
  }
  h2 {
    font-size: 1.3em;
  }
  strong {
    color: #9a4d16;
  }
  code {
    background: #f3ede2;
    color: #143a36;
  }
  img[alt~="center"] {
    display: block;
    margin: 0 auto;
  }
  .two-cols {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
    align-items: start;
  }
  .note {
    font-size: 0.72em;
    color: #4d5d5a;
  }
  .schedule-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px 28px;
    margin-top: 18px;
  }
  .schedule-col {
    display: grid;
    gap: 20px;
  }
  .schedule-card {
    background: rgba(255, 255, 255, 0.82);
    border: 2px solid #d9dfd8;
    border-left: 10px solid #d98f3d;
    border-radius: 18px;
    padding: 12px 14px;
  }
  .schedule-card h3 {
    margin: 0 0 6px 0;
    font-size: 0.9em;
    line-height: 1.25;
  }
  .schedule-card p {
    margin: 0;
    font-size: 0.68em;
    line-height: 1.35;
  }
  .term-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px 28px;
    margin-top: 18px;
  }
  .term-col {
    display: grid;
    gap: 10px;
  }
  .term-item {
    background: rgba(255, 255, 255, 0.76);
    border-radius: 14px;
    padding: 10px 14px;
    font-size: 0.9em;
  }
  table {
    font-size: 0.78em;
  }
  blockquote {
    border-left: 6px solid #d98f3d;
    background: rgba(255, 255, 255, 0.65);
    padding: 0.6em 0.9em;
  }
---

# 機械学習トレーニング
## 講義スライド

- Python基礎からミニプロジェクトまでを8回で体験
- 可視化、回帰、分類、CNN、クラスタリングを段階的に学ぶ
- AIを使っても、**結果を自分の言葉で説明できること**を重視

---

# この講義のねらい

- データ分析の流れを、手を動かしながら理解する
- 「コードを書く」だけでなく、**データを見て考える**習慣をつける
- モデルを作ったあとに、**評価して解釈する**ところまで経験する
- 最終的に、小規模な分析プロジェクトを自力で進められるようになる

---

# スケジュール

<div class="term-grid">
<div class="term-col">
<div class="term-item">1. 班分け、ガイダンス</div>
<div class="term-item">2. テーマ1 講義</div>
<div class="term-item">3. テーマ1 演習</div>
<div class="term-item">4. テーマ2 講義</div>
<div class="term-item">5. テーマ2 演習</div>
<div class="term-item">6. テーマ3 講義</div>
<div class="term-item">7. テーマ3 演習</div>
<div class="term-item">8. テーマ4 講義</div>
</div>
<div class="term-col">
<div class="term-item">9. テーマ4 演習</div>
<div class="term-item">10. テーマ5 講義</div>
<div class="term-item">11. テーマ5 演習</div>
<div class="term-item">12. テーマ6 講義</div>
<div class="term-item">13. テーマ6 演習</div>
<div class="term-item">14. テーマ7 講義</div>
<div class="term-item">15. テーマ7 演習</div>
</div>
</div>

---

# 必要な物品

- ノートパソコン

---

# データ分析の基本サイクル

![w:600 center](./assets/data_science_cycle.drawio.svg)

---

# 8回の全体ロードマップ

<div class="schedule-grid">

<div class="schedule-col">

<div class="schedule-card">
<h3>テーマ1 Python基礎・導入</h3>
<p>Notebook環境に慣れ、Pythonの基本操作とデータの見方を確認する。</p>
</div>

<div class="schedule-card">
<h3>テーマ2 可視化とEDA</h3>
<p>分布・相関・外れ値に注目し、可視化から仮説を立てる練習をする。</p>
</div>

<div class="schedule-card">
<h3>テーマ3 回帰分析の基礎</h3>
<p>数値予測の考え方を学び、線形回帰で傾向をモデル化する。</p>
</div>

<div class="schedule-card">
<h3>テーマ4 回帰モデル評価</h3>
<p>train/test 分割と評価指標を使って、モデル比較と過学習を考える。</p>
</div>

</div>

<div class="schedule-col">

<div class="schedule-card">
<h3>テーマ5 分類の基礎</h3>
<p>カテゴリ予測を体験し、混同行列を使って誤分類の中身を読む。</p>
</div>

<div class="schedule-card">
<h3>テーマ6 CNNによる画像分類</h3>
<p>画像データの特徴を踏まえ、CNNによる分類と誤分類例を観察する。</p>
</div>

<div class="schedule-card">
<h3>テーマ7 クラスタリング</h3>
<p>ラベルなしデータのまとまりを見つけ、PCAで結果を可視化する。</p>
</div>

<div class="schedule-card">
<h3>テーマ8 ミニプロジェクト</h3>
<p>EDAから解釈までを統合し、結果を説明・共有する。</p>
</div>

</div>

</div>

---

# 授業の進め方

<div class="two-cols">

<div>

## 講義パート

- 背景と目的を確認
- 重要な概念を直感的に理解
- どこを見るべきかを共有

</div>

<div>

## 演習パート

- Jupyter Notebookで実行
- 可視化やモデル構築を体験
- 結果を短く言語化して振り返る

</div>

</div>

> 目的は「正解を写すこと」ではなく、「なぜその結果になったか」を説明できるようになることです。

---

# テーマ1 Python基礎・データ分析入門

- Jupyter Notebook の使い方に慣れる
- Python の最小限の文法を確認する
- データを読み込み、眺め、簡単に可視化する

## キーワード

`変数` `print` `pandas` `可視化` `Iris`

---

# テーマ1で身につけたいこと

- セルを実行しながら試行錯誤できる
- データの列や行が何を表しているか説明できる
- ヒストグラムや散布図を見て、簡単な傾向を言える

## 例

- 花びらの長さは種類ごとに違いがありそう
- 2つの特徴量には関係がありそう

---

# テーマ2 データ可視化とEDA

- EDA は、モデル作成前の「観察」と「仮説づくり」
- 分布、相関、外れ値に注目してデータを読む
- 可視化から「効きそうな特徴量」を考える

## 使うデータ

- `Iris`

---

# EDAで何を見るか

![w:1000 center](./assets/supervised_unsupervised_map.drawio.svg)

---

# テーマ3 回帰分析の基礎

- 回帰は、**数値を予測する問題**
- まず散布図で関係を見てからモデルを考える
- 線形回帰で「傾向を式で近似する」感覚をつかむ

## 使うデータ

- `California Housing`

---

# テーマ4 回帰モデル評価

- 訓練データとテストデータの役割を理解する
- 予測できたかどうかを、指標で比較する
- 過学習のイメージをつかむ

## 比較する例

- 線形回帰
- 決定木
- ランダムフォレスト

---

# 評価で見るポイント

| 観点 | 何を見るか | 例 |
| --- | --- | --- |
| 誤差 | 予測のずれの大きさ | `RMSE`, `MAE` |
| 汎化性能 | 未知データで通用するか | train/test の差 |
| 解釈 | どんな失敗をしているか | 予測値と実測値の比較 |

---

# テーマ5 分類の基礎

- 分類は、**カテゴリを当てる問題**
- 正解率だけでなく、どの誤分類が重要かを見る
- 混同行列を使って結果を読み解く

## 使うデータ

- `Breast Cancer`

---

# テーマ6 CNNによる画像分類

- 画像は、空間構造を持つデータ
- CNN は画像の特徴を段階的に抽出する
- 誤分類画像を見ると、モデルの限界が見える

## 使うデータ

- 手書き数字データ

---

# テーマ7 クラスタリング

- クラスタリングは、**正解ラベルなしで構造を探す**
- 似たデータをまとめて眺める
- `PCA` で高次元データを見やすくする

## 使うデータ

- `Wine`

---

# 教師あり学習と教師なし学習

- 教師あり学習
  入力と正解ラベルの組から、予測ルールを学ぶ
- 教師なし学習
  正解ラベルなしで、データのまとまりや構造を見つける

## この講義での位置づけ

- 回帰・分類・CNN: 教師あり学習
- クラスタリング: 教師なし学習

---

# テーマ8 ミニデータ分析プロジェクト

- テーマ設定から解釈までを一通り実施
- EDA、モデル構築、可視化、考察を統合する
- 結果を他者に伝えるところまで含めて取り組む

## 重要な観点

- なぜその手法を選んだか
- 結果は妥当か
- 何が言えて、何はまだ言えないか

---

# AI活用の考え方

- AIの利用は可
- ただし、**そのコードや出力を理解すること**が前提
- 結果の意味や限界を、自分の言葉で説明する

## チェックしたいこと

- このグラフから何が読めるか
- この指標は何を表すか
- このモデルはどこで失敗しているか

---

# 各回で共通して大切にしたいこと

- まずデータを見る
- 可視化して傾向をつかむ
- モデルを試す
- 指標だけで終わらず、結果を解釈する
- 伝わる言葉で説明する

---

# 到達目標

- Notebook 環境で分析を進められる
- 可視化から仮説を立てられる
- 回帰・分類・CNN・クラスタリングの違いを説明できる
- モデルの結果を評価し、短く考察できる
- 小規模な分析プロジェクトをまとめられる

---

# まとめ

- この講義では、**分析の一連の流れ**を体験する
- 重要なのは、手法名を覚えることよりも、**結果を読んで考えること**
- 最終回では、その力を使って自分たちで分析を組み立てる

## 次のアクション

- テーマ1では Python と Notebook に慣れる
- わからないところは、実行しながら確認する

---

# 補足

- このスライドは `Marp` で表示する前提で作成
- 図はすべて `SVG` なので拡大しても劣化しにくい

<div class="note">
ファイル: <code>slides/course_overview_slides.md</code>
</div>
