#!/bin/sh
cd $(dirname $0)
cd ..
sudo docker build --file ./test/Dockerfile --rm -t test_env .