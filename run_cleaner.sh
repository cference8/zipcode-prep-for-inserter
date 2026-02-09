#!/bin/bash
# Activate virtual environment and run the script
cd "$(dirname "$0")"
if [ -d ".venv" ]; then
    .venv/bin/python3 main.py
else
    echo "Virtual environment not found. Please run set up first."
    exit 1
fi
