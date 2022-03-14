#!/bin/bash
app="docker.test"
docker build -t ${app} .
docker run -p 5000:80 --volume=${pwd}:/app ${app}
