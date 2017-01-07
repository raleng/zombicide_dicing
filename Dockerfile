# adapted from https://gist.github.com/tshirtman/18e64fb786c8aa1a959295cabc59c626
# build with
#     docker build -f Dockerfile -t renemilk/zombicide_dicing .
# use the produced image with
#     docker run -v your_project_dir/.buildozer:/home/dicing/.buildozer -v your_project_dir:/home/dicing/build renemilk/zombicide_dicing
# at the end of the run, the build directory in your project should contain the apk
# you can use the ~/.buildozer/ volume to cache your distributions (first usage may be longer)

FROM ubuntu:16.10

RUN groupadd -r dicing && useradd -r -m -g dicing dicing
ENV DEBIAN_FRONTEND noninteractive

RUN dpkg --add-architecture i386 &&\
    apt-get update &&\
    apt-get install -y --no-install-recommends \
        wget build-essential ccache git libncurses5:i386 libstdc++6:i386 \
        libgtk2.0-0:i386 python-jinja2 python-sh python-appdirs python-colorama \
        python3-setuptools python3-jinja2 python3-sh python3-appdirs python3-colorama \
        libpangox-1.0-0:i386 libpangoxft-1.0-0:i386 libidn11:i386 \
        python2.7 python2.7-dev python-pip openjdk-8-jdk unzip vim \
        lzma unp zlib1g-dev python-setuptools zlib1g:i386 file &&\
    pip install --upgrade cython buildozer six
ENV DEBIAN_FRONTEND teletype


#RUN chown dicing /home/dicing

ENV CRYSTAX_VER crystax-ndk-10.3.2-linux-x86_64
ENV CRYSTAX_TGZ ${CRYSTAX_VER}.tar.xz
RUN cd /opt && \
    wget -q -O- https://www.crystax.net/download/${CRYSTAX_TGZ} \
    | tar xJ

ADD minimal_spec/* /home/dicing/minimal_spec/
RUN chown -R dicing /home/dicing/
USER dicing
ENV HOME /home/dicing

RUN set -e && cd /home/dicing/minimal_spec && \
    echo y | buildozer -v android_new debug &&\
    mkdir ~/build/

VOLUME ["/home/dicing/build"]
WORKDIR "/home/dicing/build"
# ENTRYPOINT ["buildozer", "android_new", "debug"]
