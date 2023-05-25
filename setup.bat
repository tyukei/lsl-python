@echo off

REM 仮想環境の作成
python -m venv .venv
call .venv\Scripts\activate.bat

REM パッケージのインストール
pip install -r requirements.txt

REM Pythonスクリプトの実行
python gui.py

REM スクリプト実行終了後に仮想環境を無効化する
deactivate
