#!/usr/bin/env bash

docker stop ssh 2&>/dev/null || true
docker rm ssh 2&>/dev/null || true
echo "OK"
