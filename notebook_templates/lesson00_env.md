# 開発環境

このノートブックでは、学習用の開発環境が正しく使えるかを確認します。必要なライブラリの有無や、実行方法の確認に使ってください。

## 必要なもの

学習を始める前に、次のものを用意してください。

- インターネットに接続できるPC
- ブラウザ（Chrome など）
- Python 3.10 以上
- Jupyter Notebook を実行できる環境
- `pip` と `venv` を使える状態

最初に Python のバージョンを確認します。

```bash
python --version
```

## Google Colabolatory

Google Colab を使う場合は、ブラウザだけで作業を始められます。次の手順で確認してください。

1. Google アカウントでログインする。
2. Colab を開いて「新しいノートブック」を作成する。
3. 次のコードを実行して、セルの実行方法を確認する。

```python
print("Hello, Colab")
```

4. 必要に応じて `pandas` や `scikit-learn` をインストールする。

```python
!pip install pandas scikit-learn
```

## Windows

Windows では、WSL2 を使う方法が扱いやすいです。まずはどちらの方法で進めるかを決めてください。

### WSL2のインストール

WSL2 を使うと、Windows 上でも Linux に近い環境で Python を扱えます。導入は次の流れで進めます。

1. 管理者権限の PowerShell を開く。
2. 次のコマンドを実行する。

```powershell
wsl --install
```

3. 再起動後、Ubuntu などの Linux ディストリビューションを起動する。
4. ユーザー名とパスワードを設定する。
5. 次のコマンドで Python が使えるか確認する。

```bash
python3 --version
```

6. 必要なら `sudo apt update` と `sudo apt install python3-pip python3-venv` を実行する。


### jupyter notebookでプログラミング 

Jupyter Notebook を使う場合は、仮想環境を作ってから起動します。次の順で試してください。

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install jupyter pandas numpy matplotlib scikit-learn
jupyter notebook
```

起動後は、新しい Notebook を開いて次を実行します。

```python
print("Hello, Notebook")
```

セルは `Shift + Enter` で実行し、結果が下に表示されることを確認してください。

### venvでプログラミング

venv を使うと、プロジェクトごとに Python 環境を分けられます。Windows では次の手順で進めます。
#### python venvのインストール

まず、プロジェクト用のフォルダを作成してから仮想環境を作ります。

```bash
mkdir ml_training
cd ml_training
python -m venv .venv
```

その後、仮想環境を有効化します。

```powershell
.venv\Scripts\activate
```

最後に、必要なライブラリを入れます。

```bash
python -m pip install --upgrade pip
pip install jupyter pandas numpy matplotlib scikit-learn
```

#### venvの使い方

venv を有効化したら、次のように環境を確認します。

```bash
where python
python --version
```

`where python` で仮想環境の Python が先に表示されれば、正しく切り替わっています。作業が終わったら次のコマンドで終了します。

```powershell
deactivate
```

## Mac

Mac では、ターミナルから `venv` と Jupyter Notebook を使う流れが基本です。

### jupyter notebookでプログラミング 

Mac でも、仮想環境を作ってから Jupyter Notebook を起動します。

```bash
mkdir ml_training
cd ml_training
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install jupyter pandas numpy matplotlib scikit-learn
jupyter notebook
```

起動後は、新しい Notebook を作成して次を実行してください。

```python
print("Hello, Mac Notebook")
```

セルは `Shift + Enter` で実行し、結果が表示されることを確認します。

### venvでプログラミング

venv を使うと、プロジェクトごとに Python 環境を分けられます。Mac では次の流れで使います。
#### python venvのインストール

まず、仮想環境を作成します。

```bash
python3 -m venv .venv
```

次に有効化して、Python の場所を確認します。

```bash
source .venv/bin/activate
which python
```

必要なライブラリは有効化した状態でインストールします。

```bash
python -m pip install --upgrade pip
pip install jupyter pandas numpy matplotlib scikit-learn
```

#### venvの使い方

有効化したあとは、毎回ターミナルを開いたら `source .venv/bin/activate` を実行します。作業中は `python` と `pip` が仮想環境のものを使っているかを確認してください。

```bash
python --version
pip list
deactivate
```
