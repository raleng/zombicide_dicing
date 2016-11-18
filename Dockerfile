# adapted from https://gist.github.com/tshirtman/18e64fb786c8aa1a959295cabc59c626
# build with
#     docker build -f Dockerfile -t renemilk/zombicide_dicing .
# use the produced image with
#     docker run -v your_project_dir:/root/build renemilk/zombicide_dicing
# at the end of the run, the build directory in your project should contain the apk
# you can use the /root/.buildozer/ volume to cache your distributions (first usage may be longer)

FROM ubuntu:16.10

ENV HOME /root
ENV DEBIAN_FRONTEND noninteractive
RUN dpkg --add-architecture i386 &&\
    apt-get update &&\
    apt-get install -y --no-install-recommends \
        wget build-essential ccache git libncurses5:i386 libstdc++6:i386 \
        libgtk2.0-0:i386 python-jinja2 python-sh python-appdirs python-colorama \
        python3-setuptools python3-jinja2 python3-sh python3-appdirs python3-colorama \
        libpangox-1.0-0:i386 libpangoxft-1.0-0:i386 libidn11:i386 \
        python2.7 python2.7-dev python-pip openjdk-8-jdk unzip \
        lzma unp zlib1g-dev python-setuptools zlib1g:i386 &&\
    pip install --upgrade cython buildozer
ENV DEBIAN_FRONTEND teletype

RUN mkdir /root/test_project/

# RUN wget https://www.crystax.net/download/crystax-ndk-10.3.2-linux-x86_64.tar.xz 
COPY crystax-ndk-10.3.2-linux-x86_64.tar.xz /root/
RUN unp /root/crystax-ndk-10.3.2-linux-x86_64.tar.xz 1> /dev/null && \
  ln -s $PWD/crystax-ndk-10.3.2-linux-x86_64 /opt/crystax-ndk-10.3.2 && \
  rm /root/crystax-ndk-10.3.2-linux-x86_64.tar.xz
RUN cd /root/test_project && \
    echo y | buildozer init && \
    echo y | buildozer -v android_new debug &&\
    mkdir /root/build/

VOLUME ["/root/.buildozer", "/root/build"]
WORKDIR "/root/build"
ENTRYPOINT ["buildozer", "android_new", "debug"]
