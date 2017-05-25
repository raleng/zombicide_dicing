REPO = raleng/zomdie
TAG = kotlin
DOCKER = docker run --rm -it -e LOCAL_USER_ID=$(shell id -u) -v ${PWD}:/home/dicing/ $(REPO):$(TAG)

.PHONY: docker push debug release

docker:
	docker build --rm -t $(REPO):$(TAG) docker

push:
	docker push $(REPO):$(TAG)

debug: docker
	$(DOCKER) gradle build

interactive: docker
	$(DOCKER) bash

run: debug
	java -jar build/debug/zomdie.jar

all: debug
