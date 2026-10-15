#!/bin/bash
# Supervisor loop: restarts listener.py if it exits.
cd "$(dirname "$0")"
# Load runtime secrets if present (never commit this file).
if [ -f /home/box/.grokbot-home/secrets.env ]; then
  set -a
  # shellcheck disable=SC1091
  . /home/box/.grokbot-home/secrets.env
  set +a
fi
while true; do
  ./venv/bin/python listener.py
  echo "$(date '+%F %T') listener exited ($?), restarting in 10s" >> listener.log
  sleep 10
done
