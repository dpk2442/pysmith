#!/bin/sh

cd "$(dirname "$0")/.."
pytest --verbose --cov-config tox.ini --cov-report html --cov-report term --cov pysmith --html test_report.html --self-contained-html tests
