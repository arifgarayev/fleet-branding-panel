#!/bin/zsh
docker buildx build --platform linux/amd64 -f ./gunicorn.Dockerfile -t flaskapp_amd .
docker tag flaskapp_amd europe-north1-docker.pkg.dev/carapplication-311912/branded-car-verification/flaskapp_amd
docker push europe-north1-docker.pkg.dev/carapplication-311912/branded-car-verification/flaskapp_amd