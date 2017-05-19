#!/bin/bash

USER_ID=${LOCAL_USER_ID:-1000}

echo "Starting with UID : $USER_ID"
useradd --shell /bin/bash -u $USER_ID -o -c "" -m dicing && \
    adduser dicing sudo &&\
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
export HOME=/home/dicing

chown -R dicing /home/dicing

exec gosu dicing "$@"
