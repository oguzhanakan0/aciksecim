#!/bin/bash
timestamp=$(date +%s)
image="${timestamp}"
docker build -t ${image} .
docker push ${image}
