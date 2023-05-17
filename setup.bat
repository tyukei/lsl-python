@echo off

REM 仮想環境の作成
python -m venv myenv
call myenv\Scripts\activate.bat

REM パッケージのインストール
pip install matplotlib
pip install pylsl

REM スクリプト実行終了後に仮想環境を無効化する
deactivate
