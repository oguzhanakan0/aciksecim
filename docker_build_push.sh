#!/bin/bash
timestamp=$(date +%s)
image="europe-west1-docker.pkg.dev/data-rookery-387723/aciksecim-gar/aciksecim:${timestamp}"
docker build -t ${image} .
docker push ${image}