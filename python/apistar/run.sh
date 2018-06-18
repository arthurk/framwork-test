#!/usr/bin/env bash
set -ex

pipenv run uvicorn app:app
