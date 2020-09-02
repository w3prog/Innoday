#!/bin/bash

until curl -s $CAMUNDA_BASE_REST_API; do
  echo "Camunda is unavailable - sleeping"
  sleep 1
done

echo "Camunda is up - executing command"
python3 -u main.py