"""保存した家計調査・気象庁の原データから、ビールの回帰試行データと図を作る。

リポジトリのルートから:
  .venv/bin/python notebook/scripts/build_beer_weather_dataset.py

外部ネットワークへの接続は不要。東京都区部と全国平均を区別し、
全国平均には東京1地点の気象を参考指標として対応させる。
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

DATASETS = Path(__file__).resolve().parents[1] / 'datasets'
TARGET = 'ビール支出額(円)'
TEMP = '東京_月平均気温(℃)'
HUMIDITY = '東京_月平均相対湿度(%)'
RAIN = '東京_月降水量合計(mm)'


def household(source: zipfile.ZipFile, name: str, target: str = TARGET) -> pd.DataFrame:
    response = json.loads(source.read(name))
    soup = BeautifulSoup(response['table'], 'html.parser')
    records = []
    for row in soup.select('tbody tr'):
        value = row.select_one('td.stat-dbview-value')
        heading = row.select_one('th[data-unique]')
        if value is None or heading is None:
            continue
        code = heading['data-unique']
        records.append({'年月': pd.Timestamp(int(code[:4]), int(code[6:8]), 1),
                        target: float(value.get_text(strip=True).replace(',', ''))})
    result = pd.DataFrame(records).sort_values('年月').reset_index(drop=True)
    if result['年月'].duplicated().any() or result[target].isna().any():
        raise ValueError(f'家計調査の重複・欠測: {name}')
    return result


def weather(source: zipfile.ZipFile) -> pd.DataFrame:
    rows = list(csv.reader(io.StringIO(source.read('jma/tokyo_monthly_2015_2025.csv').decode('cp932'))))
    if rows[3][0] != '年月' or set(rows[2][1:]) != {'東京'}:
        raise ValueError('東京の月別CSVではありません')
    raw = pd.DataFrame(rows[5:])
    result = pd.DataFrame({'年月': pd.to_datetime(raw[0], format='%Y/%m')})
    mapping = [(TEMP, '平均気温(℃)', 1, 2), (HUMIDITY, '平均湿度(％)', 4, 5),
               (RAIN, '降水量の合計(mm)', 7, 9), ('東京_月日照時間(h)', '日照時間(時間)', 11, 13),
               ('東京_月平均風速(m/s)', '平均風速(m/s)', 15, 16)]
    for output, original, value, quality in mapping:
        if rows[3][value] != original or rows[4][quality] != '品質情報':
            raise ValueError(f'気象の列構成が変わっています: {original}')
        result[output] = pd.to_numeric(raw[value], errors='raise')
        result[output + '_品質情報'] = pd.to_numeric(raw[quality], errors='raise').astype(int)
        if not result[output + '_品質情報'].isin([5, 8]).all():
            raise ValueError(f'今回の利用方針に含まれない品質情報: {original}')
    return result


def add_calendar(frame: pd.DataFrame) -> pd.DataFrame:
    frame = frame.copy()
    frame.insert(1, '年', frame['年月'].dt.year)
    frame.insert(2, '月', frame['年月'].dt.month)
    frame['12月フラグ'] = frame['月'].eq(12).astype(int)
    return frame


def evaluate(frame: pd.DataFrame, target: str, train_end: str, test_start: str,
             test_end: str, geography: str) -> tuple[dict, dict]:
    train = frame[frame['年月'] < train_end]
    test = frame[frame['年月'].between(test_start, test_end)]
    predictions = {
        '学習期間の平均': np.full(len(test), train[target].mean()),
        '学習期間の同じ月の平均': test['月'].map(train.groupby('月')[target].mean()).to_numpy(),
    }
    models = {'気温だけ': [TEMP], '気象3変数': [TEMP, HUMIDITY, RAIN],
              '気温＋12月': [TEMP, '12月フラグ']}
    for name, columns in models.items():
        predictions[name] = LinearRegression().fit(train[columns], train[target]).predict(test[columns])
    scores = {name: float(np.sqrt(mean_squared_error(test[target], pred)))
              for name, pred in predictions.items()}
    return {'対象': geography, '目的変数': target, '学習期間': [str(train['年月'].min().date()), str(train['年月'].max().date())],
            '評価期間': [str(test['年月'].min().date()), str(test['年月'].max().date())],
            '学習月数': len(train), '評価月数': len(test), 'RMSE': scores}, predictions


def build(source_path: Path, output_dir: Path, render: bool = True) -> dict:
    with zipfile.ZipFile(source_path) as source:
        manifest = json.loads(source.read('manifest.json'))
        for record in manifest['sources']:
            if hashlib.sha256(source.read(record['file'])).hexdigest() != record['sha256']:
                raise ValueError(f'原データのSHA-256が一致しません: {record["file"]}')
        met = weather(source)
        national = household(source, 'estat/national_spending_2015_2025.json')
        tokyo = household(source, 'estat/tokyo_spending_2015_2024.json')
        quantity = household(source, 'estat/national_quantity_2015_2024.json', 'ビール購入数量(L)')
    national = add_calendar(national.merge(met, on='年月', validate='one_to_one'))
    tokyo = add_calendar(tokyo.merge(met, on='年月', validate='one_to_one'))
    quantity = add_calendar(quantity.merge(met, on='年月', validate='one_to_one'))
    for frame, end in [(national, '2025-12-01'), (tokyo, '2024-12-01'), (quantity, '2024-12-01')]:
        if not pd.DatetimeIndex(frame['年月']).equals(pd.date_range('2015-01-01', end, freq='MS')):
            raise ValueError('月の欠落・重複・期間外の値があります')
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = [(national, 'beer_national_tokyo_weather_2015_2025.csv'),
               (tokyo, 'beer_tokyo_weather_2015_2024.csv'),
               (quantity, 'beer_quantity_national_tokyo_weather_2015_2024.csv')]
    for frame, filename in outputs:
        frame.to_csv(output_dir / filename, index=False, encoding='utf-8-sig', date_format='%Y-%m-%d')
    experiments = []
    for frame, target, place in [(tokyo, TARGET, '東京都区部'), (national, TARGET, '全国'),
                                 (quantity, 'ビール購入数量(L)', '全国')]:
        result, _ = evaluate(frame, target, '2023-01-01', '2023-01-01', '2024-12-01', place)
        experiments.append(result)
    final, final_predictions = evaluate(national, TARGET, '2023-01-01', '2025-01-01', '2025-12-01', '全国')
    experiments.append(final)
    # 試行後の追加検討。2025年は既に見ているので独立な最終評価とは呼ばない。
    train = national[national['年'] <= 2024]
    test = national[national['年'] == 2025]
    columns = [TEMP, '12月フラグ', '年']
    extra_prediction = LinearRegression().fit(train[columns], train[TARGET]).predict(test[columns])
    extra = {'対象': '全国', 'モデル': '気温＋12月＋年', '学習期間': '2015〜2024年', '評価期間': '2025年',
             'RMSE_円': float(np.sqrt(mean_squared_error(test[TARGET], extra_prediction))),
             '位置付け': '2025年を見た後の追加検討。未使用データでの性能とは扱わない。'}
    report = {'retrieved_date_jst': '2026-10-30', 'experiments': experiments, 'additional_exploration': extra,
              'geography_note': '全国平均の家計と東京都区部の家計を別ファイルに保存。気象は東京1地点で、全国平均ではない。',
              'protocol_note': '2015〜2022年を学習、2023〜2024年を試行に使用。その後、気温と12月フラグのモデルを変えず2025年を確認。最後の気温＋12月＋年は追加の探索。',
              'quality_note': '欠損はなく、気象庁の正常値8と準正常値5を使用。品質情報は列として保存。',
              'dataset_sha256': {filename: hashlib.sha256((output_dir / filename).read_bytes()).hexdigest()
                                 for _, filename in outputs},
              'source_archive_sha256': hashlib.sha256(source_path.read_bytes()).hexdigest()}
    (output_dir / 'beer_regression_trial.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    if render:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from matplotlib import font_manager
        available = {font.name for font in font_manager.fontManager.ttflist}
        plt.rcParams['font.family'] = next((name for name in ['Hiragino Sans', 'Yu Gothic', 'IPAexGothic', 'DejaVu Sans'] if name in available), 'sans-serif')
        fig, axes = plt.subplots(2, 2, figsize=(13, 8))
        for is_dec, label, color in [(False, '1〜11月', 'tab:blue'), (True, '12月', 'tab:orange')]:
            part = national[national['12月フラグ'].eq(int(is_dec))]
            axes[0, 0].scatter(part[TEMP], part[TARGET], label=label, color=color, alpha=.7, s=20)
        axes[0, 0].set_xlabel('東京の月平均気温（℃）')
        axes[0, 0].set_ylabel('全国のビール支出額（円/世帯）')
        axes[0, 0].set_title('全国支出額と東京の気温（地域の範囲は異なる）')
        axes[0, 0].legend()
        axes[0, 1].plot(national['年月'], national[TARGET], color='black', linewidth=1)
        axes[0, 1].set_title('全国の月別ビール支出額：2015〜2025年')
        axes[0, 1].set_ylabel('円/世帯')
        for ax, start, end, title in [(axes[1, 0], '2023-01-01', '2024-12-01', '試行：2023〜2024年'),
                                      (axes[1, 1], '2025-01-01', '2025-12-01', '同じモデルで確認：2025年')]:
            part = national[national['年月'].between(start, end)]
            _, preds = evaluate(national, TARGET, '2023-01-01', start, end, '全国')
            ax.plot(part['年月'], part[TARGET], label='実測', color='black', marker='o', markersize=3)
            for name in ['気温だけ', '気温＋12月']:
                ax.plot(part['年月'], preds[name], label=name, linewidth=1.5)
            ax.set_title(title + '（学習はいずれも2015〜2022年）')
            ax.set_ylabel('円/世帯')
            ax.legend()
        for ax in axes.flat:
            ax.grid(alpha=.2)
            if ax is not axes[0, 0]:
                ax.tick_params(axis='x', rotation=25)
        fig.tight_layout()
        fig.savefig(output_dir / 'beer_regression_trial.png', dpi=130)
        plt.close(fig)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-zip', type=Path, default=DATASETS / 'beer_monthly_weather_sources.zip')
    parser.add_argument('--output-dir', type=Path, default=DATASETS)
    parser.add_argument('--no-render', action='store_true')
    args = parser.parse_args()
    report = build(args.source_zip, args.output_dir, not args.no_render)
    for experiment in report['experiments']:
        print(experiment['対象'], experiment['目的変数'], experiment['評価期間'],
              {name: round(value, 3) for name, value in experiment['RMSE'].items()})
    print('追加検討:', report['additional_exploration'])


if __name__ == '__main__':
    main()
