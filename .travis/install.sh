#!/bin/bash

set -e
set -x

pip install bokeh==${BOKEH_VER}
python setup.py install
