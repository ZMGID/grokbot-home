#!/bin/bash
# Idempotent start: launches the supervisor loop unless already running.
cd "$(dirname "$0")"
if [ -f supervisor.pid ] && kill -0 "$(cat supervisor.pid)" 2>/dev/null; then
  echo "already running (supervisor pid $(cat supervisor.pid))"; exit 0
fi
if pgrep -f "gmail-listener/run_loop.sh" >/dev/null; then
  echo "already running (found run_loop.sh)"; exit 0
fi
nohup setsid /workspace/gmail-listener/run_loop.sh >/dev/null 2>&1 &
echo $! > supervisor.pid
echo "started supervisor pid $!"
