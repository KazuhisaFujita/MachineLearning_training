#!/usr/bin/env python3
"""lesson04スライド3「回帰と分類、予測の形が違う」用の比較図を生成する。

左右ともノートブックと同一設定の学習用70輪（versicolor / virginica、
random_state=42・stratify・色・マーカー・軸範囲も同じ）を使い、
データは完全に共通にする。違いは与える質問だけ。
  左: 花弁の長さから花弁の幅を予測する単回帰（ŷ = wx + b、lesson03と同じ形）
  右: 花弁の長さと幅から種類を予測するフィッシャーの線形判別の境界（第5節）
右の境界の解説は第5節以降なので、この図では背景を薄く塗るだけにする。
乱数を使う分割はノートブックと同じ固定シードで、実行ごとに同じ図になる。
実行: リポジトリルートで
    .venv/bin/python slides_04/assets/generate_regression_vs_classification.py
"""
import pathlib

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import ListedColormap
from sklearn.datasets import load_iris
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

ROOT = pathlib.Path(__file__).resolve().parents[2]
ASSETS = pathlib.Path(__file__).resolve().parent

plt.style.use('seaborn-v0_8')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Hiragino Sans', 'Yu Gothic', 'Arial Unicode MS', 'DejaVu Sans']

# --- 左右共通のデータ: ノートブックと同一の学習用70輪 ---
iris = load_iris(as_frame=True)
feature_columns = ['petal length (cm)', 'petal width (cm)']
x_col, y_col = feature_columns
class_names = {1: 'versicolor', 2: 'virginica'}
colors = {1: 'tab:blue', 2: 'tab:orange'}
markers = {1: 'o', 2: '^'}

flowers = iris.frame.loc[iris.frame['target'].isin([1, 2])].copy()
X = flowers[feature_columns]
y = flowers['target']
X_train, _, y_train, _ = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y)

x_limits = (X_train[x_col].min() - 0.4, X_train[x_col].max() + 0.4)
y_limits = (X_train[y_col].min() - 0.3, X_train[y_col].max() + 0.3)


def scatter_flowers(ax):
    for label, name in class_names.items():
        subset = X_train.loc[y_train == label]
        ax.scatter(subset[x_col], subset[y_col], color=colors[label],
                   marker=markers[label], edgecolors='white', s=45,
                   label=name, zorder=3)
    ax.set_xlim(*x_limits)
    ax.set_ylim(*y_limits)
    ax.set_xlabel('花弁の長さ（cm）')
    ax.set_ylabel('花弁の幅（cm）')


fig, (ax_reg, ax_cls) = plt.subplots(1, 2, figsize=(11.2, 4.7))

# --- 左: 同じ70輪での回帰（花弁の長さ → 花弁の幅という数値） ---
reg_model = LinearRegression()
reg_model.fit(X_train[[x_col]], X_train[y_col])

scatter_flowers(ax_reg)
xs = np.linspace(x_limits[0], x_limits[1], 2)
ax_reg.plot(xs, reg_model.predict(pd.DataFrame({x_col: xs})),
            color='red', label='回帰直線 ŷ = wx + b')

new_len = 5.0
new_width = float(reg_model.predict(pd.DataFrame({x_col: [new_len]}))[0])
ax_reg.vlines(new_len, y_limits[0], new_width, color='gray',
              linestyle=':', linewidth=1.4)
ax_reg.scatter([new_len], [new_width], color='red', marker='*', s=220,
               edgecolors='white', linewidths=0.8, zorder=5)
ax_reg.annotate(f'花弁の長さ5.0cmの花\n幅の予測 {new_width:.2f} cm\n（直線の高さ=数値）',
                xy=(new_len, new_width), xytext=(new_len + 0.15, new_width - 0.62),
                fontsize=10.5, ha='left', va='center',
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=1.5),
                arrowprops=dict(arrowstyle='->', color='#444444'))
ax_reg.set_title('同じ70輪への質問「花弁の幅は何cm?」\n答えは数値（直線の「高さ」）', fontsize=12.5)
ax_reg.legend(loc='upper left', fontsize=9.5)

# --- 右: 同じ70輪での分類（花弁の長さと幅 → 種類） ---
lda_model = LinearDiscriminantAnalysis()
lda_model.fit(X_train, y_train)

# 塗りの格子（描画用。ノートブックの境界図と同じ考え方）
xx, yy = np.meshgrid(np.linspace(*x_limits, 200), np.linspace(*y_limits, 200))
grid = pd.DataFrame(np.c_[xx.ravel(), yy.ravel()], columns=feature_columns)
region = lda_model.predict(grid).reshape(xx.shape)

# 塗りは点の下（zorder=0）、点と凡例を上に保つ
ax_cls.pcolormesh(xx, yy, region, alpha=0.12,
                  cmap=ListedColormap([colors[1], colors[2]]), shading='auto',
                  zorder=0)
scatter_flowers(ax_cls)

(w1, w2), w0 = lda_model.coef_[0], float(lda_model.intercept_[0])
bx = np.array(x_limits)
ax_cls.plot(bx, -(w1 * bx + w0) / w2, color='black', linewidth=1.6,
            label='決定境界（どちら側かで種類）')

new_flower = pd.DataFrame([[5.0, 1.7]], columns=feature_columns)
new_label = int(lda_model.predict(new_flower)[0])
ax_cls.scatter(new_flower[x_col], new_flower[y_col], color='black', marker='*',
               s=220, edgecolors='white', linewidths=0.8, zorder=5)
ax_cls.annotate(f'新しい花（5.0, 1.7）\n予測: {class_names[new_label]}\n（上側・ほぼ線上）',
                xy=(5.0, 1.7), xytext=(5.15, 1.12), fontsize=10.5, ha='left', va='center',
                bbox=dict(facecolor='white', alpha=0.75, edgecolor='none', pad=1.5),
                arrowprops=dict(arrowstyle='->', color='#444444'))
ax_cls.set_title('同じ70輪への質問「種類はどれ?」\n答えは2つのうち1つ（直線の「どちら側か」）', fontsize=12.5)
ax_cls.legend(loc='upper left', fontsize=9.5)

fig.tight_layout()
fig.savefig(ASSETS / 'regression_vs_classification.png', dpi=170,
            facecolor='white')
print('saved regression_vs_classification.png')
print(f'回帰の予測: 長さ{new_len:.1f}cm → 幅{new_width:.3f}cm / '
      f'分類の予測: (5.0, 1.7) → {class_names[new_label]}')
