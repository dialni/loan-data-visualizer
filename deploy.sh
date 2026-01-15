#!/bin/bash
clear
cd src/frontend/
./publish.sh
cd ../..
sudo docker build -t ldr-backend -f src/backend.Dockerfile . 
sudo docker build -t ldr-frontend -f src/frontend.Dockerfile . 
clear
docker compose up --abort-on-container-exit