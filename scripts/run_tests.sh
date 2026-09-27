#!/usr/bin/env bash
set -e
echo "=== Running Data Warehouse Design Agent Test Suite ==="
./venv/bin/pytest tests/ -v
echo "=== Test Suite Passed ==="
