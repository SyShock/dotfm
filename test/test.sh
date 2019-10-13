#!/bin/sh
cd $(dirname $0)
cd ..
docker build --file ./test/Dockerfile --rm -t test_env .
