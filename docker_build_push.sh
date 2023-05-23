#!/bin/bash
timestamp=$(date +%s)
image="location:${timestamp}"
docker build --platform linux/amd64 -t ${image} .
docker push ${image}