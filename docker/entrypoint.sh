#!/bin/bash

USER_ID=${LOCAL_USER_ID:-1000}

echo "Starting with UID : $USER_ID"
export HOME=/home/dicing
adduser -S -s /bin/bash -u ${USER_ID} -h ${HOME} dicing

chown -R dicing $HOME

exec gosu dicing "$@"
