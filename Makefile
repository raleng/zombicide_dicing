REPO = raleng/zomdie
TAG = kotlin

.PHONY: push docker

docker:
	docker build --rm -t $(REPO):$(TAG) docker

push:
	docker push $(REPO):$(TAG)

debug: docker
	[ -d build/debug ] || mkdir -p build/debug
	docker run -it  -e LOCAL_USER_ID=$(shell id -u) -v ${PWD}:/home/dicing/build $(REPO):$(TAG) kotlinc main.kt -include-runtime -d build/debug/zomdie.jar

interactive: docker
	docker run -it  -e LOCAL_USER_ID=$(shell id -u) -v ${PWD}:/home/dicing/build $(REPO):$(TAG) bash

run: debug
	java -jar build/debug/zomdie.jar

all: debug
