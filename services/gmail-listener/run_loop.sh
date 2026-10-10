#!/bin/bash
# Supervisor loop: restarts listener.py if it exits.
cd "$(dirname "$0")"
while true; do
  ./venv/bin/python listener.py
  echo "$(date '+%F %T') listener exited ($?), restarting in 10s" >> listener.log
  sleep 10
done
