import os
import site
import sys
import customtkinter

import PyInstaller.__main__

def build():
    # customtkinterのパッケージパスを取得
    # PyInstallerではテーマファイルなどを手動で含める必要があります
    customtkinter_path = os.path.dirname(customtkinter.__file__)
    
    # OSごとの区切り文字（Windowsは ';', Mac/Linuxは ':'）
    sep = os.pathsep
    
    print(f"Building application... (CustomTkinter path: {customtkinter_path})")

    args = [
        'main.py',                           # エントリーポイント
        '--name=MVP_CRUD_App',               # 出力される実行ファイル名
        '--onefile',                         # シングルバイナリにする
        '--windowed',                        # コンソールウィンドウを非表示にする (GUIアプリ用)
        '--noconfirm',                       # 既存の出力ディレクトリを上書きする
        '--clean',                           # ビルド前にキャッシュをクリアする
        f'--add-data={customtkinter_path}{sep}customtkinter/', # customtkinterのリソースを含める
    ]
    
    PyInstaller.__main__.run(args)
    print("Build complete!")

if __name__ == "__main__":
    build()
