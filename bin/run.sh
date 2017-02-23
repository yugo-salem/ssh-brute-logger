#!/usr/bin/env bash

ROOT=$(pwd)

. ./config.env

docker run \
  --name=ssh \
  -itd --restart=always \
  -p ${SSH_PORT}:${SSH_PORT} \
  --log-driver=none \
  --env-file=config.env \
  -v ${ROOT}/src/:/opt/src/ \
  -v ${ROOT}/data/:/opt/data/ \
  -v ${ROOT}/logs/:/opt/logs/ \
  ssh-logger \
  python ./run.py
