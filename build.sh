#!/bin/bash
docker rm chanweb -f
docker build -t chandoc -f ./resources/Dockerfile .
docker run --name chanweb -d -p 4000:80 --dns-search=bwh.harvard.edu --dns=170.223.101.17 chandoc
