@echo off

REM 仮想環境のアクティブ化
call myenv\Scripts\activate.bat

REM Pythonスクリプトの実行
python main.py

REM 仮想環境の無効化
deactivate
