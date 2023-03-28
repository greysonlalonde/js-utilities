#!/bin/sh -e
cd .. && cd src
set -x
autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place . --exclude=__init__.py
isort --force-single-line-imports . && isort . && blue . && flake8 . && mypy .
