#!/usr/bin/env bash
set -ex

pipenv run hypercorn app:app -b 0.0.0.0:8000
