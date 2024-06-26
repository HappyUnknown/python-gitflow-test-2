# Using multiple Python versions
# https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python

name: push-to-master

on:
  push:
    branches:
      - 'master'
      - 'main'

jobs:
  build:

    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [
          ubuntu-latest
          # , macos-latest, windows-latest
          ]
        python-version: [
        # "pypy3.9", "pypy3.10", 
        "3.9"
        # , "3.10", "3.11" ,"3.12"
        ]
        # exclude:
        #   - os: macos-latest
        #     python-version: "3.9"
        #   - os: windows-latest
        #     python-version: "3.9"

    steps:
      - uses: actions/checkout@v4
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      # You can test your matrix by printing the current Python version
      - name: Display Python version
        run: python -c "import sys; print(sys.version)"
      - name: Installing packages
        run: python -m pip install --upgrade flask #pymongo bson flask_swagger_ui werkzeug hashlib os
      - name: Launch web
        run: python backend/web.py
        shell: sh
