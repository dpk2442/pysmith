# Pysmith

[![CI](https://github.com/dpk2442/pysmith/workflows/CI/badge.svg?branch=master)](https://github.com/dpk2442/pysmith/actions?query=workflow%3ACI)
[![Documentation Status](https://readthedocs.org/projects/pysmith/badge/?version=latest)](https://pysmith.readthedocs.io/en/latest/)

A file processing pipeline primary designed for static site generation. It is heavily inspired by
[Metalsmith](https://metalsmith.io/).

The docs can be found on Read the Docs here: https://pysmith.readthedocs.io/en/latest/.

## Installation

This library can be installed directly from Github like this:

    pip install git+https://github.com/dpk2442/pysmith.git#egg=pysmith

To install any extras use the following command:

    pip install git+https://github.com/dpk2442/pysmith.git#egg=pysmith[extra1,extra2]

## Tests

`flake8` is used for linting and `Pytest` is used for testing. To install the necessary dependencies, first run:

    pip install -r requirements_dev.txt

Then use the scripts to run linting:

    ./scripts/run_flake8.sh
    ./scripts/run_pytest.sh

If do not want to use the scripts you can use the `flake8` and `pytest` commands directly.

## Docs

To build the docs locally, first, install the necessary dependencies:

    pip install -r requirements_docs.txt

Then navigate to the `docs` folder and run:

    make html

The built docs can be found in the docs/_build/html folder.
