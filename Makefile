REPO = raleng/zomdie
TAG = latest

.PHONY: push docker

docker:
	docker build --rm -t $(REPO):$(TAG) docker

push:
	docker push $(REPO):$(TAG)

debug:
	docker run -it  -e LOCAL_USER_ID=$(shell id -u) -v ${PWD}:/home/dicing/build $(REPO):$(TAG) buildozer android debug

all: debug
