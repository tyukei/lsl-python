#!/bin/bash
python3 -m venv .venv
DIR=$(realpath $(dirname $0))
PATH=$DIR/.venv/bin/activate
source $PATH
pip install matplotlib
pip install pylsl
deactivate