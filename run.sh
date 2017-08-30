#!/bin/bash
kill $(ps aux | grep 'python main.py' | awk '{print $2}')

if [ "$1" == "stop" ]; then
  exit 0
fi

rm -rf log/*
mkdir -p log

bash -c "while true; do python main.py; done;" &> ./log/main.log &
