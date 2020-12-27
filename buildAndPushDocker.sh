#!/bin/bash

#git pull

echo "Build and Push Docker"

docker build -t $DOCKERHUB_USERNAME/hc3-display:latest .

docker login --username $DOCKERHUB_USERNAME --password $DOCKERHUB_PASSWORD

docker push $DOCKERHUB_USERNAME/hc3-display:latest
