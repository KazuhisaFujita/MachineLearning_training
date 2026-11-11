"""学習期間の説明変数どうしの関係を3組の散布図で示す。"""

import csv
import os
from pathlib import Path
from statistics import correlation

os.environ.setdefault("MPLCONFIGDIR", "/tmp/lesson03-matplotlib")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[2]
with (ROOT / "notebook/datasets/ice.csv").open(encoding="utf-8-sig") as source:
    rows = [row for row in csv.DictReader(source) if 2003 <= int(row["年"]) <= 2010]
assert len(rows) == 96

temperature = "日最高気温の平均(℃)"
humidity = "平均湿度(％)"
rain = "降水量の合計(mm)"
days = "日最高気温25℃以上日数(日)"
pairs = [
    (temperature, humidity, "日最高気温の平均（℃）", "平均湿度（%）"),
    (rain, humidity, "降水量の合計（mm）", "平均湿度（%）"),
    (temperature, days, "日最高気温の平均（℃）", "日最高気温25℃以上の日数（日）"),
]

plt.style.use("seaborn-v0_8-darkgrid")
plt.rcParams.update({"font.family": "Hiragino Sans", "font.size": 18})
fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))
for ax, (x_col, y_col, x_label, y_label) in zip(axes, pairs):
    x = [float(row[x_col]) for row in rows]
    y = [float(row[y_col]) for row in rows]
    ax.scatter(x, y, s=65, color="#4c72b0", alpha=0.65)
    ax.set_xlabel(x_label, labelpad=10)
    ax.set_ylabel(y_label, labelpad=10)
    ax.set_title(f"相関係数 r = {correlation(x, y):.2f}", pad=14)
fig.subplots_adjust(left=0.06, right=0.99, bottom=0.19, top=0.85, wspace=0.38)
fig.savefig(Path(__file__).with_name("ice_collinearity.png"), dpi=160)
plt.close(fig)
