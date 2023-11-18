.PHONY: build

include .env
export
ENV ?= local
ifeq ($(ENV), local)
	REGISTRY := localhost:5000
else
	REGISTRY := logileifs
endif

serve:
	uvicorn app.app:app \
		--log-config=${LOG_CONFIG} \
		#--ssl-certfile=cert.pem \
		#--ssl-keyfile=key.pem \
		--log-level=debug \
		--host=0.0.0.0 \
		--port=${PORT} \
		--reload

do_build:
	$(info STARTING BUILD)
	docker build --quiet -t ${REGISTRY}/${APP_NAME} .

post_build:
	$(info BUILD DONE)
	$(eval NEW_BUILD_ID:=$(shell docker images -q ${REGISTRY}/${APP_NAME} | head -n 1))
	$(eval CURRENT_COMMIT := $(shell git rev-parse --short HEAD))
	$(eval FULL_VERSION := $(VERSION).$(COMMIT).$(NEW_BUILD_ID))
	$(info NEW VERSION is $(FULL_VERSION))
	$(eval LINE_NUMBER:=$(shell cat .env | grep -n BUILD_ID | cut -f1 -d:))
	@sed -i "$(LINE_NUMBER)s/.*/BUILD_ID=${NEW_BUILD_ID}/" .env
	$(eval LINE_NUMBER := $(shell cat .env | grep -n COMMIT | cut -f1 -d:))
	@sed -i "$(LINE_NUMBER)s/.*/COMMIT=${CURRENT_COMMIT}/" .env
	$(eval LINE_NUMBER := $(shell cat .env | grep -n FULL_VERSION | cut -f1 -d:))
	@sed -i "$(LINE_NUMBER)s/.*/FULL_VERSION=${FULL_VERSION}/" .env

build: do_build post_build tag

tag:
	docker tag ${REGISTRY}/${APP_NAME} ${REGISTRY}/${APP_NAME}:$(FULL_VERSION)

push:
	docker push ${REGISTRY}/${APP_NAME}:latest
	docker push ${REGISTRY}/${APP_NAME}:$(FULL_VERSION)

run:
	docker run -p 8000:8000 ${REGISTRY}/${APP_NAME}:latest

cert:
	openssl req -nodes -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365

deploy: build push
	@helm upgrade -i $(RELEASE_NAME) \
		-f helm/values.yaml \
		-f helm/values-${ENV}.yaml \
		--set image_tag=${FULL_VERSION} \
		helm/ --create-namespace

undeploy:
	helm uninstall $(RELEASE_NAME)

template:
	# need to include .env again since BUILD_ID might have changed
	$(eval include .env)
	helm template -f ./helm/values.yaml \
		-f ./helm/values-local.yaml \
		--set image_tag=${FULL_VERSION} \
		--set registry=${REGISTRY} ./helm/
