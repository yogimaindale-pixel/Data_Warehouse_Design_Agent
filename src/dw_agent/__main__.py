# Module docstring explaining python -m dw_agent entrypoint execution
"""Package entry point allowing execution via `python -m dw_agent` command."""

# Import sys module to pass process exit status codes back to operating system
import sys
# Import main CLI entrypoint function from cli module
from dw_agent.cli import main

# Check if script is executed directly from command line
if __name__ == "__main__":
    # Execute main CLI function and pass exit code to system
    sys.exit(main())

