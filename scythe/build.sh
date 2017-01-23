#!/bin/bash

rm -f sf tm
cp ./bin/sf ./bin/tm .
docker build --build-arg userid="$(id -u)" -t tmtest .
rm -f sf tm
