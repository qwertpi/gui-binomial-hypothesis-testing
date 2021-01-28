coverage run --branch --include=$PWD/*.py --omit=distribution.py -m pytest; coverage html; coverage xml -o coverage/coverage.xml
bandit *.py -x test*
pylint -j 0 --ignore-patterns=test* --disable=W0312,C0303,C0301,C0103,C0114 *.py
