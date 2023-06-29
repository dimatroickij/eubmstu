#!/bin/sh

ssh -p 2222 -o StrictHostKeyChecking=no server@$IP_ADDRESS << 'ENDSSH'
  cd /home/server/eubmstu
  docker compose -f docker-compose.prod.yml stop
  export $(cat .env | xargs)
  docker login -u $CI_REGISTRY_USER -p $CI_JOB_TOKEN $CI_REGISTRY
  docker pull $IMAGE:eubmstu
  docker compose -f docker-compose.prod.yml up -d
ENDSSH