#!/bin/bash
python3 -m venv .venv
DIR=$(realpath $(dirname $0))
PATH=$DIR/.venv/bin/activate
source $PATH
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 gui.py
deactivate