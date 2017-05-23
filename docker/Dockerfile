# adapted from https://gist.github.com/tshirtman/18e64fb786c8aa1a959295cabc59c626
# build with
#     docker build -f Dockerfile -t renemilk/zombicide_dicing .
# use the produced image with
#     docker run -v your_project_dir/.buildozer:/home/dicing/.buildozer -v your_project_dir:/home/dicing/build renemilk/zombicide_dicing
# at the end of the run, the build directory in your project should contain the apk
# you can use the ~/.buildozer/ volume to cache your distributions (first usage may be longer)

FROM rayyildiz/kotlin:latest

# grab gosu for easy step-down from root
RUN apk add --update ca-certificates curl gnupg && \
    gpg --keyserver pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4 && \
    ARCH=`uname -m`; if [ $ARCH == "x86_64" ]; then export ARCH="amd64"; else export ARCH="i386"; fi && \
    curl -o /usr/local/bin/gosu -SL "https://github.com/tianon/gosu/releases/download/1.6/gosu-$ARCH" && \
    curl -o /usr/local/bin/gosu.asc -SL "https://github.com/tianon/gosu/releases/download/1.6/gosu-$ARCH.asc" && \
    gpg --verify /usr/local/bin/gosu.asc && \
	rm /usr/local/bin/gosu.asc && \
	chmod +x /usr/local/bin/gosu && \
    apk del ca-certificates curl gnupg && \
    rm -rf /var/cache/apk/*


VOLUME ["/home/dicing/build"]
WORKDIR "/home/dicing/build"
ADD entrypoint.sh /usr/local/bin/
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
