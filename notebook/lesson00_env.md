# 開発環境

この資料では、授業で使う Python 実行環境を準備し、Notebook が動くことを確認します。初回はまず Google Colab を使えるようにし、必要なら手元の PC にローカル環境を用意してください。

## この回の目標

- Google Colab またはローカル Jupyter Notebook を起動できる
- セルを実行して結果を確認できる
- 今後の演習で使う基本ライブラリを準備できる

## 事前に用意するもの

- インターネット接続
- ブラウザ
- Google アカウント（Colab を使う場合）
- 十分な空き容量のある PC（ローカル環境を使う場合）

## プログラミングの手順

### 一般的な流れ

プログラミングは、コンピュータ上で動くソフトウェアを作るための基本的な作業です。一般的には、**プログラムコードを書き、それを実行する**という流れで進めます。プログラムコードは、**プログラミング言語**と呼ばれる人工的に設計された言語を使って記述します。

プログラムコードは、基本的には文字で構成されたテキストファイルです。コードの作成には、文字を編集するための**テキストエディタ**や、プログラムコードの作成に適した機能を備えた**コードエディタ**を使用します。

プログラムコードを作成したら、次にそのコードを実行します。実行の仕組みはプログラミング言語によって異なりますが、代表的なものとして、**コンパイル言語**と**インタプリタ言語**があります。

コンパイル言語では、プログラムコードをあらかじめコンピュータが実行できる形式に翻訳する**コンパイル**という作業を行い、その後にプログラムを実行します。一方、インタプリタ言語では、**インタプリタ**と呼ばれるソフトウェアがプログラムコードを読み取りながら実行します。

この授業で使用する **Python** は、一般にインタプリタ言語として利用されます。そのため、基本的には次のような流れでプログラミングを行います。

```text
コーディング
    |
    v
   実行
```

一方、本授業では **Notebook** という形式も活用します。Notebook は、ノートのように**説明文とプログラムコードを一緒に記述できる環境**です。記述したコードは、その場ですぐに実行できます。

そのため、説明文を読みながらプログラムコードを確認するだけでなく、コードの一部を実際に実行し、結果を確認しながら学習できます。特に、コードを少しずつ変更して試したり、実行結果を比較したりできることが Notebook の大きな利点です。

Notebook を使うには、大きく分けて 2 つの方法があります。1 つは、Web ブラウザから利用できる Google Colaboratory（Google Colab） を使う方法です。もう 1 つは、自分の PC に JupyterLab をインストールして、Web ブラウザから利用する方法です。

## まずは Google Colab を使う

授業をすぐ始めるだけなら、Google Colab が最も簡単です。ブラウザだけで Python を実行できます。

### Colab を開く手順

1. [Google Colab](https://colab.research.google.com/?hl=ja) を開く。
2. Google アカウントでログインする。
3. 「新しいノートブック」を作成する。
4. 最初のセルに次のコードを入力する。

```python
print("Hello, Colab")
```

5. `Shift + Enter` で実行する。
6. セルの下に `Hello, Colab` と表示されれば準備完了です。

### Colab / Jupyter の基本操作

| 操作 | ショートカット | 説明 |
|---|---|---|
| セルを実行 | `Shift + Enter` | 現在のセルを実行する |
| 保存 | `Cmd + S` / `Ctrl + S` | ノートブックを保存する |
| コマンドモードへ戻る | `Esc` | セル操作のモードに切り替える |
| 下にセルを追加 | `B` | コマンドモードで使う |
| 上にセルを追加 | `A` | コマンドモードで使う |
| セルを削除 | `dd` | コマンドモードで `d` を 2 回押す |

### ノートブックでよく見る画面要素

- メニューバー: 保存、セル操作、ランタイム操作などを行う
- ツールバー: 実行や追加など、よく使う操作をまとめた領域
- セル: コードや説明文を入力する単位
- 出力欄: 実行結果やエラーメッセージが表示される場所

## ローカル環境を使う場合

長時間の実行、手元ファイルの利用、ネットワーク制限のある作業では、PC に Python と Jupyter を入れて開発する方が適しています。

ローカル環境では、まず仮想環境 `venv` を作成し、その中に必要なライブラリを入れます。

### インストールするライブラリ

この授業では、主に次のライブラリを使います。

- `jupyterlab`
- `numpy`
- `pandas`
- `matplotlib`
- `scikit-learn`

## Windows の場合

Windows では、WSL2 上に Python 環境を作る方法を推奨します。既に Python を直接使える環境がある場合は、その環境を使っても構いません。

### WSL2 の導入

1. 管理者権限で PowerShell を開く。
2. 次のコマンドを実行する。

```powershell
wsl --install
```

3. 再起動後、Ubuntu などの Linux 環境を起動する。
4. ユーザー名とパスワードを設定する。
5. Python が使えるか確認する。

```bash
python3 --version
```

6. 必要なら次を実行する。

```bash
sudo apt update
sudo apt install python3-pip python3-venv
```

### Windows で Jupyter を使う手順

リポジトリをクローンしたフォルダの中で仮想環境を用意します。

```bash
cd MachineLearning_training
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install jupyterlab numpy pandas matplotlib scikit-learn
jupyter lab
```

WSL2 ではブラウザが自動で開かないことがあります。その場合は、ターミナルに表示された URL を Windows 側のブラウザへ貼り付けてください。表示例は次のようになります。

```text
http://localhost:8888/?token=xxxxxxxxxxxxxxx
```

起動後は新しい Notebook を作成し、次を実行して確認します。

```python
print("Hello, Notebook")
```

### Windows での確認コマンド

仮想環境が有効な状態で、次を実行してください。

```bash
which python
python --version
pip list
```

作業終了後は次で仮想環境を抜けます。

```bash
deactivate
```

## Mac の場合

Mac は標準で Python 3 が使えるため、追加の Python インストールは不要です。ターミナルから Python 仮想環境を作成し、その中で Jupyter Notebook を起動します。

### Mac で Jupyter を使う手順

```bash
cd MachineLearning_training
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install jupyterlab numpy pandas matplotlib scikit-learn
jupyter lab
```

通常は `jupyter lab` 実行後にブラウザが開きます。自動で開かない場合は、ターミナルに表示された URL をブラウザへ貼り付けてください。

起動後は新しい Notebook を作成し、次を実行してください。

```python
print("Hello, Notebook")
```

### Mac での確認コマンド

```bash
which python
python --version
pip list
```

作業終了後は次を実行します。

```bash
deactivate
```

## うまく動かないときの確認

- `python --version` または `python3 --version` で Python が見つかるか
- `which python` または `where python` で仮想環境の Python を使っているか
- `pip install ...` 実行時にエラーが出ていないか
- `jupyter lab` 実行後に URL が表示されているか
- Notebook のセルを実行したとき、エラーメッセージが出ていないか

## 最低限の動作確認

環境構築が終わったら、次の 3 点を確認してください。

1. Python のバージョンが表示される。
2. Notebook が開く。
3. 次のコードが実行できる。

```python
import numpy as np
import pandas as pd

print("環境準備OK")
print(np.array([1, 2, 3]).mean())
print(pd.DataFrame({"a": [1, 2], "b": [3, 4]}))
```

上のコードが動けば、この授業の最初の演習を始める準備はできています。
