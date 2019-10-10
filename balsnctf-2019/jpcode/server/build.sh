#!/bin/sh
docker build --no-cache --tag jpcode:latest .
docker run --name jpcode_challenge -p 127.0.0.1:19091:19091/tcp -d --restart=always jpcode:latest
