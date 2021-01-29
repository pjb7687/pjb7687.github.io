#!/bin/bash
python .ci/get_citations.py
python .ci/get_covid19stats.py
yarn run sass
sphinx-build -a source build