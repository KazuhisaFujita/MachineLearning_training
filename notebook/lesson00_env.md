# 開発環境

このノートブックでは、学習用の開発環境が正しく使えるかを確認します。必要なライブラリの有無や、実行方法の確認に使ってください。

## 必要なもの

学習を始める前に、次のものを用意してください。

- インターネットに接続できるPC
- ブラウザ（Chrome など）
- 充電器
- Google Colab または Jupyter Notebook を使える環境
- Python 3.10 以上
- `pip` と `venv` を使える状態

最初に Python のバージョンを確認します。

```bash
python --version
```

## Google Colab

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

## Jupyter Notebookの基本操作

Jupyter が起動するとブラウザでノートブックのリスト画面が表示されます。ここから実際にコードを書く方法をまとめます。

### ファイルの作成と保存

1. **新しいノートブックを作成する**
   - 右上の「New」→「Python 3 (ipykernel)」または同様のオプションを選択する。

2. **ファイル名を変更する**
   - 上部の「Untitled」となっている部分をクリックして名前を入力する。例: `lesson01_intro.ipynb`

3. **ファイルを保存する**
   - Jupyter は自動保存されますが、`Ctrl + S` (`Cmd + S`) で明示的に保存できます。

### ノートブック編集画面

ノートブックを開くと次のような構成になっています。

- **メニューバー**: ファイル操作・セル操作・カーネル管理など
- **ツールバー**: よく使うボタンの並列表示
- **セル**: コードやテキストを入力するブロック
- **出力領域**: 各セルの実行結果

### セルの種類と操作

Jupyter のセルには2つのタイプがあります。

| ツール | Mac/Linux          | Windows           | 機能               |
|--------|---------------------|--------------------|--------------------|
| 再生   | `Shift + Enter`     | `Shift + Enter`    | セルを実行         |
| コマンド   | `Esc`               | `Esc`              | モードに切り替え   |
| 保存   | `Cmd + S`          | `Ctrl + S`        | 保存する           |

### ノートブックの操作

1. **セルを追加する**
   - 現在のセルを選択した状態で、メニューの「Insert」から、「Below」または「Above」を選ぶ。
   - またはコマンドモードで `B` キーで下に、`A` キーで上に新しいセルを追加できます。

2. **セルを削除する**
   - メニューの Edit → Delete Cell を選択する。
   - コマンドモードでも「dd」(dキーを2回) で削除可能。

3. **セルをコピー・貼り付けする**
   - コマンドモードで `c` でコピー、`v` でペースト。

4. **セルの下に実行結果を表示する**
   - `Shift + Enter` が一番確実な方法です。

### カーネルの管理

*カーネルは Python のエンジン部分です。*

- **再起動:** 「Kernel」→「Restart」をクリックする。
- **シャットダウン:** 「File」→「Close and Halt Notebook」を選択する。
  - ノートブックを閉じ、そのノートブックのカーネルを終了します。

5. **終了**
   - Jupyter を使用した後は、ターミナルウィンドウで `Ctrl + C` を2回押してシャットダウンする。

### ファイル管理リスト

ファイルリスト画面に戻ると:
- 各フォルダやディレクトリ名をクリックするだけで移動できます。
- フォルダやファイルを右クリックすると削除/リネームなどの操作が可能です。

---

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

WSL2の場合、ブラウザが自動起動しないことがあります。その場合は以下の手順で手動で開きます。

1. `jupyter notebook` を実行すると、ターミナル上に以下のようなメッセージが表示されます:

   ```
   http://localhost:8888/?token=xxxxxxxxxxxxxxx
   ```

2. Windows 側のブラウザを開き、上記の URL をそのままコピーしてアドレスバーに貼り付ける。

> **注意**: WSL2内部で起動した Jupyter は、Windows 側から `localhost` でアクセスできますが、ポート番号とトークンを毎回確認する必要があります。ターミナルの出力を巻き戻さないようご注意ください。

> **ブラウザが自動起動しない場合**  
> ターミナルに `--no-browser` が指定されていたら削除するか、代わりに以下のコマンドを試してください:
> ```bash
> jupyter notebook --no-browser
> ```

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

Macの場合、`jupyter notebook`実行後、自動的にブラウザが起動しJupyterの画面が開きます。もし自動で開かない場合は、ターミナルに表示されたURL (例: `http://localhost:8888/?token=xxx`) をブラウザに貼り付けて手動でアクセスしてください。

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
