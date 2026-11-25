#!/usr/bin/env python3
"""lesson05講義スライド用の図と指標JSONを生成する。

ノートブック本文のコードセルを上から順にexecし、図が出るセルの直後にPNGを保存する。
軸範囲・色・乱数シード・エポック数までノートブックと同一の図になる。Notebookファイルの
保存済み出力には依存しない。実行: リポジトリルートで

    .venv/bin/python slides_05/assets/generate_slides_assets.py

ノートブックと追加で描く説明図（relu.png / network_architecture.png /
reg_vs_linear.png / cls_prob_new_flower.png）も同じ実行から作る。
"""
import importlib.util
import json
import os
import pathlib
import warnings

import matplotlib
matplotlib.use('Agg')

ROOT = pathlib.Path(__file__).resolve().parents[2]
NOTEBOOK = ROOT / 'notebook' / 'lesson05_neural_network_basic_template.ipynb'
ASSETS = pathlib.Path(__file__).resolve().parent

# 図を保存するセル（ノートブック内のcell index）→ [(ファイル名, dpi), ...]（セル内の図の順）
FIGURES = {
    4:  [('ice_scatter.png', 200)],
    10: [('reg_curves.png', 150), ('reg_learning_curve.png', 200)],
    12: [('reg_test.png', 170)],
    15: [('iris_scatter.png', 200)],
    20: [('cls_boundaries.png', 150), ('cls_learning_curve.png', 180)],
    22: [('cls_test.png', 200)],
}

# ノートブックは 'datasets/ice.csv' を相対パスで読むため、notebookディレクトリに移動する
os.chdir(ROOT / 'notebook')

# ノートブックは表示用に IPython.display.display を使う。IPythonが無い環境では
# 標準出力に出すだけの差し替えを用意する（図の描画には影響しない）。
import sys
import types
if importlib.util.find_spec('IPython') is None:
    _display_module = types.ModuleType('IPython.display')

    def display(*objects, **kwargs):
        for obj in objects:
            print(obj)

    _display_module.display = display
    _ipython_module = types.ModuleType('IPython')
    _ipython_module.display = _display_module
    # matplotlib等が対話環境の検出に使うget_ipython()は「対話環境なし」を返す
    _ipython_module.get_ipython = lambda: None
    _ipython_module.version_info = (9, 0, 0)
    sys.modules['IPython'] = _ipython_module
    sys.modules['IPython.display'] = _display_module
    print('IPythonが無い環境のため、display()は標準出力に差し替えました')

# ------------------------------------------------------------------ フォント
# ノートブックは 'font.family = sans-serif' に macOS向けフォントを並べる。matplotlibは
# 'sans-serif' を解決ときに最も合う1フォントだけを選ぶため、font.sans-serifの2番目以降は
# 文字単位のフォールバックに使われない（日本語が豆腐になる）。そこで font.family 自体に
# 実在するフォント名を並べ、先頭に見つからない文字を後続フォントで補う。
# 先頭はノートブックと同じ macOS向けフォントなので、macOSでは描画が変わらない。
JP_FONTS = ['Hiragino Sans', 'Yu Gothic', 'Noto Sans CJK JP', 'Noto Sans JP', 'Meiryo']
LATIN_FONT = 'DejaVu Sans'
LAST_RESORT_FONTS = ['Droid Sans Fallback']


def available_font_names():
    from matplotlib import font_manager
    return {f.name for f in font_manager.fontManager.ttflist}


def apply_font_fallback():
    """実在する日本語フォントを font.family の先頭に、Latin用を2番目に置く。"""
    import matplotlib.pyplot as plt
    installed = available_font_names()
    jp = [f for f in JP_FONTS if f in installed]
    families = jp + [LATIN_FONT] + [f for f in LAST_RESORT_FONTS
                                     if f in installed and f not in jp]
    plt.rcParams['font.family'] = families
    return families


def savefig_checked(fig, path, dpi):
    """グリフ欠落（豆腐）を警告ではなくエラーとして扱う保存。"""
    with warnings.catch_warnings():
        warnings.simplefilter('error', UserWarning)
        fig.savefig(path, dpi=dpi)


FAMILIES = None

nb = json.loads(NOTEBOOK.read_text(encoding='utf-8'))
ns = {}
saved = []

for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] != 'code':
        continue
    import matplotlib.pyplot as plt
    before = set(plt.get_fignums())
    exec(compile(''.join(cell['source']), f'cell{i}', 'exec'), ns)
    # ノートブックのフォント指定を、この環境で実際に効く形に置き換える（毎セル後。
    # ノートブック側がrcParamsへ再代入しても追従するため）
    families = apply_font_fallback()
    if FAMILIES != families:
        print('font.family =', families)
        FAMILIES = families
    if i in FIGURES:
        new_figures = [plt.figure(n) for n in sorted(set(plt.get_fignums()) - before)]
        if len(new_figures) != len(FIGURES[i]):
            raise RuntimeError(f'cell {i}: 図が{len(new_figures)}枚、期待は{len(FIGURES[i])}枚')
        for fig, (name, dpi) in zip(new_figures, FIGURES[i]):
            savefig_checked(fig, ASSETS / name, dpi)
            saved.append(name)
            print('saved', name)
        plt.close('all')

import numpy as np
import pandas as pd
import torch
import matplotlib.pyplot as plt

# ---------------------------------------------------------------- 指標の収集
reg_history_df = ns['reg_history_df']
cls_history_df = ns['cls_history_df']
ice_test = ns['ice_test']
ice_target = ns['ice_target']
ice_feature = ns['ice_feature']

from sklearn.metrics import mean_absolute_error, mean_squared_error

reg_best_row = reg_history_df.loc[ns['reg_best_epoch']]
cls_best_row = cls_history_df.loc[ns['cls_best_epoch']]
ice_test_predictions = ns['ice_test_predictions']

metrics = {
    'environment': {
        'python': __import__('sys').version.split()[0],
        'torch': torch.__version__,
        'numpy': np.__version__,
        'pandas': pd.__version__,
        'matplotlib': matplotlib.__version__,
        'sklearn': __import__('sklearn').__version__,
        'notebook': 'notebook/lesson05_neural_network_basic_template.ipynb',
        'note': '乱数シード42で再実行した結果。ノートブックの保存済み出力（PyTorch 2.14.1, macOS）と'
                '下表の数値はすべて一致した。環境違いで数値は変わることがある。',
    },
    'regression': {
        'feature': ice_feature,
        'target': ice_target,
        'n': {'train': int(len(ns['ice_train'])), 'valid': int(len(ns['ice_valid'])),
              'test': int(len(ice_test))},
        'periods': {'train': '2003-2008', 'valid': '2009-2010', 'test': '2011-2012'},
        'architecture': [1, 16, 16, 1],
        'loss': 'MSELoss（標準化した購入額）',
        'optimizer': 'Adam lr=0.01',
        'epochs': int(ns['reg_epochs']),
        'snapshot_epochs': [int(e) for e in ns['reg_snapshot_epochs']],
        'best_epoch': int(ns['reg_best_epoch']),
        'best_valid_rmse': round(float(reg_best_row['valid_rmse']), 1),
        'rmse_at_snapshots': [
            {'epoch': int(e),
             'train_rmse': round(float(reg_history_df.loc[e, 'train_rmse']), 1),
             'valid_rmse': round(float(reg_history_df.loc[e, 'valid_rmse']), 1)}
            for e in ns['reg_snapshot_epochs']
        ],
        'test': [
            {'model': name,
             'MAE': round(float(mean_absolute_error(ice_test[ice_target], p)), 1),
             'RMSE': round(float(np.sqrt(mean_squared_error(ice_test[ice_target], p))), 1)}
            for name, p in ice_test_predictions.items()
        ],
        'prediction_at_25c': round(float(ns['reg_predict_yen'](
            ns['as_float_tensor'](ns['ice_x_scaler'].transform(pd.DataFrame({ice_feature: [25.0]}))))[0]), 1),
        'linear_regression': {
            'coef': round(float(ns['ice_linear_model'].coef_[0]), 1),
            'intercept': round(float(ns['ice_linear_model'].intercept_), 1),
        },
        'train_mean_target': round(float(ns['ice_train'][ice_target].mean()), 1),
        # スライド15: 学習用期間を気温で分けたときの購入額の分布
        'train_target_by_temperature': {
            label: {'n': int(len(part)), 'mean': round(float(part[ice_target].mean()), 1),
                    'min': int(part[ice_target].min()), 'max': int(part[ice_target].max())}
            for label, part in [
                ('15c_or_below', ns['ice_train'][ns['ice_train'][ice_feature] <= 15]),
                ('above_15_to_20c', ns['ice_train'][(ns['ice_train'][ice_feature] > 15)
                                                    & (ns['ice_train'][ice_feature] <= 20)]),
                ('above_25c', ns['ice_train'][ns['ice_train'][ice_feature] > 25]),
            ]
        },
        # スライド20: 選んだエポック以降（それ自身を含む）の検証RMSEの変動範囲
        'valid_rmse_from_best_epoch': {
            'from_epoch': int(ns['reg_best_epoch']),
            'min': round(float(reg_history_df['valid_rmse'].iloc[int(ns['reg_best_epoch']):].min()), 1),
            'max': round(float(reg_history_df['valid_rmse'].iloc[int(ns['reg_best_epoch']):].max()), 1),
        },
        # スライド21: 学習済みNNの予測曲線の傾き（気温ごとの予測額）
        'curve_prediction_yen': {
            f'{t}c': round(float(ns['reg_predict_yen'](ns['as_float_tensor'](
                ns['ice_x_scaler'].transform(pd.DataFrame({ice_feature: [float(t)]}))))[0]), 1)
            for t in [10, 15, 25, 30]
        },
        # スライド18: 学習前（epoch 0）の予測曲線がほぼ横ばいであること
        'curve_at_epoch0_yen': {
            'min': round(float(np.min(ns['reg_snapshots'][0])), 1),
            'max': round(float(np.max(ns['reg_snapshots'][0])), 1),
        },
        # スライド24: テスト各月の実測とNNの予測
        'test_by_month': [
            {'month': f'{int(year)}-{int(month):02d}', 'actual': float(actual),
             'predicted': round(float(pred), 1)}
            for year, month, actual, pred in zip(ice_test['年'], ice_test['月'],
                                                 ice_test[ice_target], ns['ice_nn_prediction'])
        ],
        'test_months_predicted_below_actual': int(
            (np.asarray(ns['ice_nn_prediction']) < ice_test[ice_target].to_numpy()).sum()),
    },
    'classification': {
        'features': ns['iris_features'],
        'classes': list(ns['iris'].target_names),
        'n': {'train': int(len(ns['iris_X_train'])), 'valid': int(len(ns['iris_X_valid'])),
              'test': int(len(ns['iris_X_test']))},
        'class_counts': {
            'train': {ns['iris'].target_names[k]: int(v)
                      for k, v in ns['iris_y_train'].value_counts().sort_index().items()},
            'valid': {ns['iris'].target_names[k]: int(v)
                      for k, v in ns['iris_y_valid'].value_counts().sort_index().items()},
            'test': {ns['iris'].target_names[k]: int(v)
                     for k, v in ns['iris_y_test'].value_counts().sort_index().items()},
        },
        'architecture': [2, 16, 16, 3],
        'loss': 'CrossEntropyLoss（3クラスのスコア）',
        'optimizer': 'Adam lr=0.02',
        'epochs': int(ns['cls_epochs']),
        'snapshot_epochs': [int(e) for e in ns['cls_snapshot_epochs']],
        'best_epoch': int(ns['cls_best_epoch']),
        'best_valid_loss': round(float(cls_best_row['valid_loss']), 3),
        'at_snapshots': [
            {'epoch': int(e),
             'train_loss': round(float(cls_history_df.loc[e, 'train_loss']), 3),
             'valid_loss': round(float(cls_history_df.loc[e, 'valid_loss']), 3),
             'train_accuracy': round(float(cls_history_df.loc[e, 'train_accuracy']), 3),
             'valid_accuracy': round(float(cls_history_df.loc[e, 'valid_accuracy']), 3)}
            for e in ns['cls_snapshot_epochs']
        ],
        'valid_accuracy_at_best_epoch': round(float(cls_best_row['valid_accuracy']), 3),
        # スライド35: 選んだエポック以降（それ自身を含む）の検証損失の変動範囲
        'valid_loss_from_best_epoch': {
            'from_epoch': int(ns['cls_best_epoch']),
            'min': round(float(cls_history_df['valid_loss'].iloc[int(ns['cls_best_epoch']):].min()), 3),
            'max': round(float(cls_history_df['valid_loss'].iloc[int(ns['cls_best_epoch']):].max()), 3),
        },
        # スライド32: epoch 0（学習前）の検証用30輪への予測の内訳
        'valid_predictions_at_epoch0': {
            ns['iris'].target_names[k]: int(v)
            for k, v in zip(*np.unique(ns['cls_valid_snapshots'][0], return_counts=True))
        },
        # スライド31: 識別領域の図で、グリッドの各クラス面積の割合（背景色の根拠）
        'grid_class_share_at_snapshots': {
            str(int(e)): {ns['iris'].target_names[k]: round(float((grid == k).mean()), 3)
                          for k in range(len(ns['iris'].target_names))}
            for e, grid in ns['cls_snapshots'].items()
        },
        # スライド34: 検証正解率が最大のエポック（検証損失が最小のエポックとは限らない）
        'valid_accuracy_max': {
            'epoch': int(cls_history_df['valid_accuracy'].idxmax()),
            'accuracy': round(float(cls_history_df['valid_accuracy'].max()), 3),
        },
        'test': {
            'accuracy': round(float(ns['iris_test_correct'].mean()), 3),
            'correct': int(ns['iris_test_correct'].sum()),
            'total': int(len(ns['iris_y_test'])),
            'one_flower_points': round(100 / len(ns['iris_y_test']), 1),
            'misclassified': [
                {'petal_length': float(r[ns['iris_x_col']]), 'petal_width': float(r[ns['iris_y_col']]),
                 'actual': str(a), 'predicted': str(p)}
                for (_, r), a, p in zip(ns['iris_X_test'].loc[~ns['iris_test_correct']].iterrows(),
                                        ns['iris_y_test'].to_numpy()[~ns['iris_test_correct']],
                                        ns['iris_test_prediction'][~ns['iris_test_correct']])
                for a, p in [(ns['iris'].target_names[a], ns['iris'].target_names[p])]
            ],
        },
        'new_flower': {
            'petal_length': 5.0, 'petal_width': 1.7,
            'predicted': str(ns['iris'].target_names[int(np.argmax(ns['new_probabilities']))]),
            'probabilities': {name: float(p) for name, p in
                              zip(ns['iris'].target_names, ns['new_probabilities'])},
            # 仮の花の座標は、テスト用30輪のどの花と重なるか（スライド38の注記用）
            'same_position_in_test': [
                {'actual': str(ns['iris'].target_names[actual]), 'correct': bool(ok)}
                for (_, row), actual, ok in zip(ns['iris_X_test'].iterrows(),
                                                ns['iris_y_test'].to_numpy(),
                                                ns['iris_test_correct'])
                if float(row[ns['iris_x_col']]) == 5.0 and float(row[ns['iris_y_col']]) == 1.7
            ],
        },
    },
}
(ASSETS / 'metrics.json').write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding='utf-8')
print('saved metrics.json')

# ------------------------------------------------------------ 説明用の追加図
C_TEXT = '#243532'
C_ACCENT = '#9a4d16'
C_GREEN = '#143a36'

# 1) 活性化関数の形（講義資料1のステップ関数、資料2のシグモイドとReLU）
fig, ax = plt.subplots(figsize=(7.2, 4.2))
a = np.linspace(-4, 4, 401)
ax.plot(a, np.where(a > 0, 1, 0), color='#8a8f8c', linewidth=1.8, linestyle=':',
        label='ステップ関数（パーセプトロン）')
ax.plot(a, 1 / (1 + np.exp(-a)), color='#4f7d74', linewidth=2.2, label='シグモイド σ(a)')
ax.plot(a, np.maximum(a, 0), color=C_ACCENT, linewidth=3, label='ReLU h(a)=max(0, a)')
ax.axhline(0, color='#b8ccc3', linewidth=1)
ax.axvline(0, color='#b8ccc3', linewidth=1)
ax.set_xlabel('入力 a（重みの総和）')
ax.set_ylabel('出力 h(a)')
ax.set_ylim(-0.6, 4.2)
ax.set_yticks([0, 1, 2, 3, 4])
ax.set_title('活性化関数の形（今回はReLU）')
ax.legend(loc='upper left', fontsize=9)
ax.annotate('負は0のまま\n（この先は学習に効かない）', xy=(-2.2, 0), xytext=(-3.9, 1.6),
            fontsize=9, color=C_ACCENT,
            arrowprops=dict(arrowstyle='->', color=C_ACCENT, lw=1.2))
ax.annotate('正は傾き1で流す', xy=(2.4, 2.4), xytext=(0.4, 3.5), fontsize=9, color=C_ACCENT,
            arrowprops=dict(arrowstyle='->', color=C_ACCENT, lw=1.2))
plt.tight_layout()
savefig_checked(fig, ASSETS / 'relu.png', 200)
plt.close(fig)
print('saved relu.png')

# 2) 2つのネットワークの構造図（回帰と分類で最後の出力と損失だけが違う）
fig, axes = plt.subplots(1, 2, figsize=(12.8, 4.6))


def draw_network(ax, n_in, n_out, in_footer, out_footer, title, subtitle):
    """隠れ層の16個まで実際に描く構造図。ノード数と列の見出しは別指定。"""
    xs = [0.02, 0.34, 0.66, 0.98]
    top, bottom = 0.88, 0.26

    def column(count, x):
        if count == 1:
            return [(x, (top + bottom) / 2)]
        return [(x, y) for y in np.linspace(top, bottom, count)]

    columns = [column(n_in, xs[0]), column(16, xs[1]), column(16, xs[2]), column(n_out, xs[3])]
    for left, right in zip(columns, columns[1:]):
        for x0, y0 in left:
            for x1, y1 in right:
                ax.plot([x0, x1], [y0, y1], color='#c6d4cb', linewidth=0.4, alpha=0.6, zorder=1)
    for nodes in columns:
        for x, y in nodes:
            ax.scatter([x], [y], s=115, facecolor='#edf3ef', edgecolor=C_GREEN,
                       linewidth=1.1, zorder=2)
    headers = ['入力', '隠れ層', '隠れ層', '出力']
    footers = [in_footer, ['Linear + ReLU', '16個'], ['Linear + ReLU', '16個'], out_footer]
    for x, header, footer in zip(xs, headers, footers):
        ax.text(x, 0.955, header, ha='center', va='bottom', fontsize=15,
                color=C_GREEN, fontweight='bold')
        ax.text(x, 0.175, '\n'.join(footer), ha='center', va='top', fontsize=13, color=C_TEXT)
    ax.set_title(title, fontsize=18, color=C_GREEN, pad=12)
    ax.text(0.5, -0.03, subtitle, ha='center', va='top', fontsize=13.5, color=C_ACCENT,
            transform=ax.transAxes)
    ax.set_xlim(-0.08, 1.08)
    ax.set_ylim(0, 1)
    ax.axis('off')


draw_network(axes[0], n_in=1, n_out=1, in_footer=['気温', '1個'], out_footer=['購入額', '1個'],
             title='アイスクリーム（回帰）',
             subtitle='損失 = MSE（標準化した購入額）／ 読み方 = 円へ戻した数値')
draw_network(axes[1], n_in=2, n_out=3, in_footer=['長さ・幅', '2個'],
             out_footer=['3クラスの', 'スコア'],
             title='Iris（分類）',
             subtitle='損失 = 交差エントロピー／ 読み方 = 最大のスコアの種類')
fig.suptitle('同じ構造、違うのは最後の出力と損失', fontsize=18, color=C_GREEN)
plt.tight_layout(rect=(0, 0.07, 1, 0.93))
savefig_checked(fig, ASSETS / 'network_architecture.png', 160)
plt.close(fig)
print('saved network_architecture.png')

# 3) 学習済みNNの予測曲線と、lesson03型の単回帰直線（同じ学習期間で比較）
linear_coef = metrics['regression']['linear_regression']['coef']
linear_intercept = metrics['regression']['linear_regression']['intercept']
linear_label = (f"単回帰 ŷ = {linear_coef}x "
                f"{'+' if linear_intercept >= 0 else '−'} {abs(linear_intercept)}（同じ学習用で直線）")
fig, ax = plt.subplots(figsize=(7.6, 4.6))
ax.scatter(ns['ice_train'][ice_feature], ns['ice_train'][ice_target], color='tab:blue',
           alpha=0.55, s=34, label='学習用（2003〜2008年）', zorder=2)
ax.scatter(ns['ice_valid'][ice_feature], ns['ice_valid'][ice_target], color='tab:orange',
           marker='^', alpha=0.8, s=42, label='検証用（2009〜2010年）', zorder=2)
ax.plot(ns['ice_line'][ice_feature],
        ns['ice_linear_model'].predict(ns['ice_line'][[ice_feature]]),
        color='#7a7a7a', linestyle='--', linewidth=2.2, zorder=3, label=linear_label)
ax.plot(ns['ice_line'][ice_feature], ns['reg_snapshots'][0], color='#b0a89a', linewidth=1.8,
        linestyle='-.', zorder=3, label='NN 学習前（epoch 0）')
ax.plot(ns['ice_line'][ice_feature], ns['reg_predict_yen'](ns['reg_line_tensor']),
        color=C_ACCENT, linewidth=2.8, zorder=4,
        label=f"NN 学習後（epoch {metrics['regression']['best_epoch']}・検証で選択）")
ax.set_xlabel('日最高気温の月平均（℃）')
ax.set_ylabel('平均購入額（円）')
ax.set_title('直線（単回帰）と曲線（ニューラルネットワーク）')
ax.legend(fontsize=9, loc='upper left')
plt.tight_layout()
savefig_checked(fig, ASSETS / 'reg_vs_linear.png', 190)
plt.close(fig)
print('saved reg_vs_linear.png')

# 4) 仮の花（長さ5.0cm・幅1.7cm）のクラス確率
fig, ax = plt.subplots(figsize=(6.4, 3.6))
names = list(ns['iris'].target_names)
probs = [float(p) for p in ns['new_probabilities']]
bars = ax.bar(names, probs, color=['#3b6fb5', '#e08a2e', '#3f8f5f'], width=0.6)
for bar, p in zip(bars, probs):
    # 非常に小さい確率は「0.000」に見えないよう、有効数字で書く
    label = f'{p:.3f}' if p >= 0.001 else f'{p:.2e}'
    ax.text(bar.get_x() + bar.get_width() / 2, p + 0.02, label, ha='center',
            fontsize=11, color=C_TEXT)
ax.axhline(0.5, color='#8a8f8c', linestyle=':', linewidth=1.2)
ax.text(2.45, 0.52, '0.5', fontsize=9, color='#6b7b74')
ax.set_ylim(0, 0.85)
ax.set_ylabel('モデルが出した確率')
ax.set_title('仮の花（長さ5.0cm・幅1.7cm）のクラス確率')
plt.tight_layout()
savefig_checked(fig, ASSETS / 'cls_prob_new_flower.png', 200)
plt.close(fig)
print('saved cls_prob_new_flower.png')

print('\n=== metrics ===')
print(json.dumps(metrics, ensure_ascii=False, indent=2)[:1500])
