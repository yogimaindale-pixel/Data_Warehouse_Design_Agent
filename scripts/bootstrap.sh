#!/usr/bin/env bash
set -e
echo "=== Bootstrapping Data Warehouse Design Agent Environment ==="
python3 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt pytest
echo "=== Bootstrap Complete ==="
