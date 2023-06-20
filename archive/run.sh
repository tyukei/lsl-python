#!/bin/sh
DIR=$(realpath $(dirname $0))
PATH=$DIR/.venv/bin/activate
source $PATH
python3 gui.py
deactivate
