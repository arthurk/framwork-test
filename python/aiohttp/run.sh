#!/usr/bin/env bash
set -ex

pipenv run gunicorn app:app --worker-class aiohttp.GunicornUVLoopWebWorker
