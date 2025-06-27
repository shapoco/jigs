# jigs

治具などの雑多な3Dモデル。

----

## CadQuery (CQ-Editor) の使用方法

### 初期設定 (Ubuntu24.04.1 LTS / WSL2)

CQ-Editor を使用する前に毎回以下を実行してください。

```bash
source ./venv-setup.shrc
```

初回は venv (仮想環境) に CQ-Editor がインストールされます。

また、`CQ-editor` が `$(pwd)/venv/bin/CQ-editor` のエイリアスになります。
エイリアスは端末を閉じるまで有効です。

### CQ-Editor によるファイルの開き方

初期設定を実施した後、以下を実行します。
`path/to/script.cq.py` はスクリプトファイルのパスです。

```bash
CQ-editor path/to/script.cq.py &
```

モデルがレンダリングされない場合は ▶ ボタンをクリックしてみてください。

以降はファイルが更新されるたびにスクリプト内の `show_object()` の呼び出しに従って再描画されます。

> [!NOTE]
> 以下のようなエラーが表示される場合、パッケージが不足している可能性があります。
>
> ```
> qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
> This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.
> ```
>
> Qt のことはよく分からないですが、「[PyQt5をUbuntuで使うときにGUI周りでエラー (WSL2)](https://qiita.com/momomo_rimoto/items/83917d3f9f5dd35457e1)」を参考に以下のパッケージを入れたところ解決しました。
>
> ```bash
> sudo apt install \
>   libxkbcommon-x11-0 \
>   libxcb-icccm4 \
>   libxcb-image0 \
>   libxcb-keysyms1 \
>   libxcb-render-util0 \
>   libxcb-xinerama0
> ```

