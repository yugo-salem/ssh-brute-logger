#!/usr/bin/env bash

tail -f ./logs/log.json | jq "."
