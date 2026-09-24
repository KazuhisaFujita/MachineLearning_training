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

藤田 一寿

---
# 概要

- Python基礎から発表までを15回で体験
- 可視化、回帰、分類、ニューラルネットワーク、CNN、クラスタリングを段階的に学ぶ
- AIを使っても、**結果を自分の言葉で説明できること**を重視

---

# この講義のねらい

- データ分析の基本的な流れを、手を動かしながら理解する
- 「コードを書く」だけでなく、**データを見て考える**習慣をつける
- モデルを作ったあとに、**評価して解釈する**ところまで経験する
- 最終的に、興味を持った分析結果を図・指標・考察で説明できるようになる

---

# スケジュール

<div class="term-grid">
<div class="term-col">
<div class="term-item">1. 班分け、ガイダンス</div>
<div class="term-item">2. テーマ1 Python基礎・導入</div>
<div class="term-item">3. テーマ2 可視化とEDA</div>
<div class="term-item">4. テーマ3 回帰分析 講義</div>
<div class="term-item">5. テーマ3 回帰分析 演習</div>
<div class="term-item">6. テーマ4 分類の基礎 講義</div>
<div class="term-item">7. テーマ4 分類の基礎 演習</div>
<div class="term-item">8. テーマ5 ニューラルネットワーク 講義</div>
</div>
<div class="term-col">
<div class="term-item">9. テーマ5 ニューラルネットワーク 演習</div>
<div class="term-item">10. テーマ6 CNNによる画像分類 講義</div>
<div class="term-item">11. テーマ6 CNNによる画像分類 演習</div>
<div class="term-item">12. テーマ7 クラスタリング 講義</div>
<div class="term-item">13. テーマ7 クラスタリング 演習</div>
<div class="term-item">14. 発表準備：興味を持った分析をまとめる</div>
<div class="term-item">15. 発表会</div>
</div>
</div>

---

# 向いている人

- 人工知能の基礎技術を習得したい人
- データサイエンスに興味がある人
- 数学やプログラミングが好きな人
