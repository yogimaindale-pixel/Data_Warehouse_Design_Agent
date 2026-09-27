#!/usr/bin/env python3
"""Run demo wrapper script."""

import sys
import os
from scripts.seed_demo import seed_demo_project
from dw_agent.cli import main as cli_main

if __name__ == "__main__":
    scenario = sys.argv[1] if len(sys.argv) > 1 else "ecommerce"
    demo_path = f"./demo_{scenario.replace('-', '_')}"
    print(f"--- Seeding Demo Scenario: {scenario} ---")
    seed_demo_project(demo_path, scenario)
    
    sys.argv = ["dw_agent", "design", "--project", demo_path, "--dialect", "sqlite"]
    print(f"--- Executing DW Agent Design Pipeline on {demo_path} ---")
    exit_code = cli_main()
    if exit_code == 0:
        print(f"\nSUCCESS: Demo '{scenario}' completed! Deliverables written to {demo_path}/output/")
    else:
        print(f"\nFAILED: Demo '{scenario}' failed with exit code {exit_code}")
    sys.exit(exit_code)
