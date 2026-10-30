"""保存済みの公式原データから、東京エリアの電力需要と東京の時別気象を結合する。

例（リポジトリのルートから、ネット接続なしで再作成）:
  .venv/bin/python notebook/scripts/build_tepco_power_weather.py

日時はすべて日本標準時。電力のTIMEは区間開始、気象の日時は区間終了。
原データの数値は補間せず、気象庁の品質情報も残す。
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import zipfile

import pandas as pd

DATASETS = Path(__file__).resolve().parents[1] / 'datasets'
STEM = 'tepco_power_weather_2024_2025'
POWER_COLUMNS = ['DATE', 'TIME', '当日実績(万kW)', '予測値(万kW)', '使用率(%)', '供給力(万kW)']
# CSVは値・品質情報・均質番号などを複数列に分けて格納している。
WEATHER_COLUMNS = [
    ('東京_気温(℃)', '気温(℃)', 1, 2),
    ('東京_相対湿度(%)', '相対湿度(％)', 4, 5),
    ('東京_降水量(mm)', '降水量(mm)', 7, 9),
    ('東京_風速(m/s)', '風速(m/s)', 11, 12),
    ('東京_日照時間(h)', '日照時間(時間)', 16, 18),
]


def read_power(source: zipfile.ZipFile) -> pd.DataFrame:
    records = []
    files = sorted(name for name in source.namelist() if name.startswith('tepco/') and name.endswith('.zip'))
    if len(files) != 24:
        raise ValueError(f'電力の月別ZIPが24件ありません: {len(files)}')
    for name in files:
        with zipfile.ZipFile(io.BytesIO(source.read(name))) as month:
            for daily_name in sorted(month.namelist()):
                if not daily_name.endswith('.csv'):
                    continue
                rows = list(csv.reader(io.StringIO(month.read(daily_name).decode('cp932'))))
                headers = [i for i, row in enumerate(rows) if row == POWER_COLUMNS]
                if len(headers) != 1:
                    raise ValueError(f'1時間ごとの表を特定できません: {daily_name}')
                hourly_rows = rows[headers[0] + 1:headers[0] + 25]
                if len(hourly_rows) != 24 or any(len(row) != len(POWER_COLUMNS) for row in hourly_rows):
                    raise ValueError(f'1日24時間の表ではありません: {daily_name}')
                records.extend(hourly_rows)
    frame = pd.DataFrame(records, columns=POWER_COLUMNS)
    frame['日時'] = pd.to_datetime(frame['DATE'] + ' ' + frame['TIME'], format='%Y/%m/%d %H:%M')
    for column in POWER_COLUMNS[2:]:
        frame[column] = pd.to_numeric(frame[column], errors='raise')
    return frame.sort_values('日時').reset_index(drop=True)


def read_weather(source: zipfile.ZipFile) -> pd.DataFrame:
    frames = []
    files = sorted(name for name in source.namelist() if name.startswith('jma/') and name.endswith('.csv'))
    if len(files) != 24:
        raise ValueError(f'気象の月別CSVが24件ありません: {len(files)}')
    for name in files:
        rows = list(csv.reader(io.StringIO(source.read(name).decode('cp932'))))
        if rows[3][0] != '年月日時' or set(rows[2][1:]) != {'東京'}:
            raise ValueError(f'東京の時別CSVではありません: {name}')
        raw = pd.DataFrame(rows[6:])
        frame = pd.DataFrame({'気象観測日時': pd.to_datetime(raw[0], format='%Y/%m/%d %H:%M:%S')})
        for output_name, source_name, value_index, quality_index in WEATHER_COLUMNS:
            if rows[3][value_index] != source_name or rows[5][quality_index] != '品質情報':
                raise ValueError(f'気象の列構成が変わっています: {name}, {source_name}')
            values = raw[value_index].replace('', pd.NA)
            frame[output_name] = pd.to_numeric(values, errors='raise')
            frame[output_name + '_品質情報'] = pd.to_numeric(raw[quality_index], errors='raise').astype(int)
        frames.append(frame)
    return pd.concat(frames, ignore_index=True).sort_values('気象観測日時').reset_index(drop=True)


def build(source_path: Path, output_path: Path) -> dict:
    with zipfile.ZipFile(source_path) as source:
        manifest = json.loads(source.read('manifest.json'))
        for record in manifest['sources']:
            if hashlib.sha256(source.read(record['file'])).hexdigest() != record['sha256']:
                raise ValueError(f'原データのSHA-256が一致しません: {record["file"]}')
        power = read_power(source)
        weather = read_weather(source)
    expected = pd.date_range('2024-01-01', '2026-01-01', inclusive='left', freq='h')
    if not pd.DatetimeIndex(power['日時']).equals(expected):
        raise ValueError('電力の日時に重複・欠落・範囲外の値があります')
    if not pd.DatetimeIndex(weather['気象観測日時']).equals(expected + pd.Timedelta(hours=1)):
        raise ValueError('気象の日時に重複・欠落・範囲外の値があります')
    power['気象観測日時'] = power['日時'] + pd.Timedelta(hours=1)
    combined = power.merge(weather, on='気象観測日時', how='left', validate='one_to_one', indicator=True)
    if not combined['_merge'].eq('both').all():
        raise ValueError('結合できない気象データがあります')
    combined = combined.drop(columns='_merge')
    combined = combined[['日時'] + POWER_COLUMNS + ['気象観測日時'] + [name for item in WEATHER_COLUMNS for name in (item[0], item[0] + '_品質情報')]]
    for column in POWER_COLUMNS[2:]:
        if combined[column].isna().any():
            raise ValueError(f'電力の欠損があります: {column}')
    for name, *_ in WEATHER_COLUMNS:
        bad = combined[name + '_品質情報'].ne(8)
        if combined.loc[bad, name].notna().any():
            raise ValueError(f'品質情報が正常値以外の数値があります。利用方針の確認が必要です: {name}')
    # 元教材の1か月分は保存したまま、今回取得した同月の値との一致を確認する。
    legacy_path = output_path.parent / 'tepco_power_usage_202508.csv'
    legacy_equal = None
    if legacy_path.exists():
        legacy = pd.read_csv(legacy_path, encoding='utf-8-sig')
        legacy['日時'] = pd.to_datetime(legacy['DATE'] + ' ' + legacy['TIME'], format='%Y/%m/%d %H:%M')
        left = combined.set_index('日時').loc[legacy['日時'], POWER_COLUMNS[2:]].reset_index(drop=True)
        right = legacy[POWER_COLUMNS[2:]].reset_index(drop=True)
        legacy_equal = left.equals(right)
        if not legacy_equal:
            raise ValueError('新規取得した2025年8月の電力数値が既存教材と異なります')
    weather_names = [item[0] for item in WEATHER_COLUMNS]
    missing_mask = combined[weather_names].isna().any(axis=1)
    missing_rows = combined.loc[missing_mask, ['日時', '気象観測日時'] + weather_names].astype(object)
    missing_rows = missing_rows.where(pd.notna(missing_rows), None)
    report = {
        'period_jst': ['2024-01-01 00:00:00', '2025-12-31 23:00:00'],
        'rows': len(combined),
        'columns': combined.columns.tolist(),
        'rows_by_year': {str(year): int(count) for year, count in combined.groupby(combined['日時'].dt.year).size().items()},
        'missing_values': {name: int(count) for name, count in combined.isna().sum().items() if count},
        'quality_counts': {name: {str(code): int(count) for code, count in combined[name + '_品質情報'].value_counts().items()} for name, *_ in WEATHER_COLUMNS},
        'rows_with_any_weather_missing': int(missing_mask.sum()),
        'missing_weather_rows': missing_rows.to_dict(orient='records'),
        'legacy_august_2025_power_values_match': legacy_equal,
        'join_rule': 'JST: TEPCO interval start + 1 hour = JMA observation time; rainfall and sunshine cover that interval; temperature/humidity are endpoint observations, wind is the preceding 10-minute mean.',
        'interpolation': 'none',
        'source_archive': source_path.name,
        'source_archive_sha256': hashlib.sha256(source_path.read_bytes()).hexdigest(),
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    combined.to_csv(output_path, index=False, encoding='utf-8-sig', date_format='%Y-%m-%d %H:%M:%S')
    report['dataset_sha256'] = hashlib.sha256(output_path.read_bytes()).hexdigest()
    report_path = output_path.with_suffix('.json')
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str, allow_nan=False) + '\n')
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-zip', type=Path, default=DATASETS / f'{STEM}_sources.zip')
    parser.add_argument('--output', type=Path, default=DATASETS / f'{STEM}.csv')
    args = parser.parse_args()
    report = build(args.source_zip, args.output)
    print(json.dumps({key: report[key] for key in ['rows', 'rows_by_year', 'missing_values', 'rows_with_any_weather_missing', 'legacy_august_2025_power_values_match']}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
