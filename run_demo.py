#!/usr/bin/env python3
# Module docstring explaining demo execution wrapper script
"""Run demo wrapper script seeding a sample project directory and running the end-to-end DW Design Agent pipeline."""

# Import sys for command-line arguments and system exit
import sys
# Import os for directory path manipulation
import os
# Import seed project generator helper
from scripts.seed_demo import seed_demo_project
# Import CLI entrypoint main function
from dw_agent.cli import main as cli_main

# Main script entrypoint execution block
if __name__ == "__main__":
    # Determine requested scenario ('ecommerce' or 'banking') from CLI argument
    scenario = sys.argv[1] if len(sys.argv) > 1 else "ecommerce"
    demo_path = f"./demo_{scenario.replace('-', '_')}"
    
    print(f"--- Seeding Demo Scenario: {scenario} ---")
    seed_demo_project(demo_path, scenario)
    
    # Simulate CLI command args: dw_agent design --project <demo_path> --dialect sqlite
    sys.argv = ["dw_agent", "design", "--project", demo_path, "--dialect", "sqlite"]
    print(f"--- Executing DW Agent Design Pipeline on {demo_path} ---")
    
    # Run main CLI pipeline
    exit_code = cli_main()
    if exit_code == 0:
        print(f"\nSUCCESS: Demo '{scenario}' completed! Deliverables written to {demo_path}/output/")
    else:
        print(f"\nFAILED: Demo '{scenario}' failed with exit code {exit_code}")
    sys.exit(exit_code)

