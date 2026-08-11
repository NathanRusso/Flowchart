#!/bin/sh

docker stop flowchart-test

docker rm flowchart-test

docker build -t flowchart-maker .

docker run --name flowchart-test -p 8080:8080 --env-file .env flowchart-maker