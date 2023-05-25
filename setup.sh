#!/bin/bash
python3 -m venv .venv
DIR=$(realpath $(dirname $0))
PATH=$DIR/.venv/bin/activate
source $PATH
python3 -m pip install --upgrade pip
pip install matplotlib
pip install pylsl
pip install PySimpleGUI
python3 main-mac.py
deactivate