#!/bin/bash
cd "$(dirname "$0")"
pkill -f "gmail-listener/run_loop.sh"; pkill -f "gmail-listener/venv/bin/python listener.py"; pkill -f "python listener.py"
rm -f supervisor.pid; echo stopped
