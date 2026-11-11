"""4つの気象と購入額の散布図を、学習期間だけで作成する。"""

import csv
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/lesson03-matplotlib")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[2]
with (ROOT / "notebook/datasets/ice.csv").open(encoding="utf-8-sig") as source:
    rows = [row for row in csv.DictReader(source) if 2003 <= int(row["年"]) <= 2010]

assert len(rows) == 96
features = [
    ("日最高気温の平均(℃)", "日最高気温の平均（℃）"),
    ("降水量の合計(mm)", "降水量の合計（mm）"),
    ("平均湿度(％)", "平均湿度（%）"),
    ("日最高気温25℃以上日数(日)", "日最高気温25℃以上の\n日数（日）"),
]
y = [float(row["アイスクリームの平均購入額"]) for row in rows]

plt.style.use("seaborn-v0_8-darkgrid")
plt.rcParams.update({"font.family": "Hiragino Sans", "font.size": 17})
fig, axes = plt.subplots(1, 4, figsize=(20, 7.3), sharey=True)
for ax, (column, label) in zip(axes, features):
    x = [float(row[column]) for row in rows]
    ax.scatter(x, y, s=65, color="#4c72b0", alpha=0.65)
    ax.set_xlabel(label, fontsize=17, labelpad=12)
    ax.set_ylim(200, 1550)
    ax.set_yticks([400, 600, 800, 1000, 1200, 1400])
axes[0].set_ylabel("平均購入額（円）", labelpad=12)
fig.subplots_adjust(left=0.065, right=0.99, bottom=0.21, top=0.97, wspace=0.13)
fig.savefig(Path(__file__).with_name("ice_extra_scatter.png"), dpi=160)
plt.close(fig)
