#!/usr/bin/env python3
"""lesson04講義スライド用の図と指標JSONを生成する。

ノートブック本文のコードセルを順番に実行し、図が出るセルの直後にPNGを保存する。
軸範囲・色・乱数シードまでノートブックと同一の図になる。Notebookファイルの
保存済み出力には依存しない。実行: リポジトリルートで
    .venv/bin/python slides_04/assets/generate_slides_assets.py
または matplotlib を備えた Python で実行する。"""
import json
import pathlib

import matplotlib
matplotlib.use('Agg')

ROOT = pathlib.Path(__file__).resolve().parents[2]
NOTEBOOK = ROOT / 'notebook' / 'lesson04_classification_basic_template.ipynb'
ASSETS = pathlib.Path(__file__).resolve().parent

# 図を保存するセル（ノートブック内のcell index）→ ファイル名 / dpi
FIGURES = {
    6:  ('train_scatter.png', 176),
    9:  ('knn_votes.png', 176),
    11: ('knn_boundary.png', 176),
    14: ('k_boundaries.png', 140),
    15: ('k_accuracy.png', 220),
    20: ('boundary_compare.png', 150),
    25: ('test_compare.png', 150),
    28: ('sigmoid.png', 190),
    31: ('prob_map.png', 176),
}

nb = json.loads(NOTEBOOK.read_text(encoding='utf-8'))
ns = {}
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] != 'code':
        continue
    exec(compile(''.join(cell['source']), f'cell{i}', 'exec'), ns)
    if i in FIGURES:
        import matplotlib.pyplot as plt
        name, dpi = FIGURES[i]
        plt.gcf().savefig(ASSETS / name, dpi=dpi)
        plt.close('all')
        print('saved', name)

import numpy as np
from sklearn.metrics import confusion_matrix

y_test_np = ns['y_test'].to_numpy()
metrics = {'train_n': int(len(ns['X_train'])), 'test_n': int(len(ns['X_test'])), 'models': {}}
for key, name in [('knn', 'kNN（k=5）'), ('lda', 'フィッシャーの線形判別'), ('logistic', 'ロジスティック回帰')]:
    model = ns[f'{key}_model']
    predicted = model.predict(ns['X_test'])
    cm = confusion_matrix(y_test_np, predicted, labels=[1, 2])
    tn, fp, fn, tp = (int(v) for v in cm.ravel())
    metrics['models'][name] = {
        'train_accuracy': round(float((model.predict(ns['X_train']) == ns['y_train'].to_numpy()).mean()), 3),
        'test_accuracy': round(float((predicted == y_test_np).mean()), 3),
        'TP': tp, 'FP': fp, 'FN': fn, 'TN': tn,
        'precision': round(tp / (tp + fp), 3),
        'recall': round(tp / (tp + fn), 3),
        'specificity': round(tn / (tn + fp), 3),
        'false_positive_rate': round(fp / (tn + fp), 3),
    }
metrics['new_flower'] = {
    'petal_length_cm': 5.0, 'petal_width_cm': 1.7,
    'knn_prediction': ns['class_names'][ns['knn_new_label']],
    'lda_prediction': ns['class_names'][ns['lda_new_label']],
}
metrics['lda'] = {
    'w': [round(float(v), 2) for v in ns['lda_model'].coef_[0]],
    'w0': round(float(ns['lda_model'].intercept_[0]), 2),
    'centers': {ns['class_names'][label]: {col: round(float(ns['centers'][label][col]), 2)
                                           for col in ns['feature_columns']}
                for label in ns['class_names']},
}
metrics['logistic'] = {
    'w': [round(float(v), 2) for v in ns['logistic_model'].coef_[0]],
    'w0': round(float(ns['logistic_model'].intercept_[0]), 2),
}
metrics['k_sweep'] = [
    {'k': int(k), 'train_accuracy': round(float(r['学習用の正解率']), 3),
     'valid_accuracy': round(float(r['検証用の正解率']), 3)}
    for k, r in ns['k_results_df'].iterrows()
]
(ASSETS / 'metrics.json').write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding='utf-8')
print('saved metrics.json')
