REPO = raleng/zomdie
TAG = kotlin

.PHONY: push docker

docker:
	docker build --rm -t $(REPO):$(TAG) docker

push:
	docker push $(REPO):$(TAG)

release:
	docker run -it  -e LOCAL_USER_ID=$(shell id -u) -v ${PWD}:/home/dicing/build $(REPO):$(TAG) buildozer android release

debug:
	docker run -it  -e LOCAL_USER_ID=$(shell id -u) -v ${PWD}:/home/dicing/build $(REPO):$(TAG) buildozer android debug

interactive: docker
	docker run -it  -e LOCAL_USER_ID=$(shell id -u) -v ${PWD}:/home/dicing/build $(REPO):$(TAG) bash

all: debug
