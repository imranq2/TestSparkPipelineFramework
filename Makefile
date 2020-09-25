LANG=en_US.utf-8

export LANG

BRANCH=$(shell git rev-parse --abbrev-ref HEAD)
VERSION=$(shell cat VERSION)
VENV_NAME=venv
GIT_HASH=${CIRCLE_SHA1}

.PHONY:venv
venv:
	python3 -m venv $(VENV_NAME)

.PHONY:devsetup
devsetup:venv
	source $(VENV_NAME)/bin/activate && \
    pip install --upgrade pip && \
    pip install --upgrade -r requirements.txt

.PHONY:test
test:
	pytest tests

.PHONY:proxies
proxies:
	python3 venv/lib/python3.8/site-packages/spark_pipeline_framework/proxy_generator/generate_proxies.py