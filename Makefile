LANG=en_US.utf-8

export LANG

BRANCH=$(shell git rev-parse --abbrev-ref HEAD)
VERSION=$(shell cat VERSION)
VENV_NAME=venv
GIT_HASH=${CIRCLE_SHA1}
PACKAGES_FOLDER=venv/lib/python3.8/site-packages

-include ${PACKAGES_FOLDER}/spark_pipeline_framework/Makefile.spark
-include ${PACKAGES_FOLDER}/spark_pipeline_framework/Makefile.docker

.PHONY:venv
venv:
	python3 -m venv $(VENV_NAME)

.PHONY:devsetup
devsetup:venv
	source $(VENV_NAME)/bin/activate && \
    pip install --upgrade pip && \
    pip install --upgrade -r requirements.txt

.PHONY:update
update:
	source $(VENV_NAME)/bin/activate && \
	pip install --upgrade -r requirements.txt && \
	pip install --upgrade sparkpipelineframework

.PHONY:tests
tests:
	source $(VENV_NAME)/bin/activate && \
	pytest tests

.PHONY:proxies
proxies:
	source $(VENV_NAME)/bin/activate && \
	python3 ${PACKAGES_FOLDER}/spark_pipeline_framework/proxy_generator/generate_proxies.py

.PHONY:up
up:
	docker-compose -p sparkpipelineframework -f ${PACKAGES_FOLDER}/spark_pipeline_framework/docker-compose.yml up --detach && \
	sleep 5 && \
	open http://localhost:8080/

.PHONY:down
down:
	docker-compose -p sparkpipelineframework -f ${PACKAGES_FOLDER}/spark_pipeline_framework/docker-compose.yml down

.PHONY:init
init: installspark docker devsetup

