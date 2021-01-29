#!/bin/bash
python .ci/get_citations.py
python .ci/get_covid19stats.py
sphinx-build -a source build
