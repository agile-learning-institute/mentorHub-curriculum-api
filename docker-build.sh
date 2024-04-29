#!/bin/bash

echo "Building Docker Image"
docker build --file Dockerfile --tag ghcr.io/agile-learning-institute/mentorhub-curriculum-api:latest .
if [ $? -ne 0 ]; then
    echo "Docker build failed"
    exit 1
fi

# Run the containers
mh up curriculum
