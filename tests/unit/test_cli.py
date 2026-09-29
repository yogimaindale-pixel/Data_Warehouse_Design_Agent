# Module docstring explaining unit tests for CLI entrypoint commands
"""Unit tests for dw_agent CLI subcommands (init, explain, design)."""

# Import unittest framework module
import unittest
# Import tempfile and shutil for sandbox directory cleanup
import tempfile
import shutil
# Import sys for CLI argument simulation
import sys
from pathlib import Path
# Import main CLI function
from dw_agent.cli import main

# Test case suite for CLI subcommands
class TestCLI(unittest.TestCase):
    def setUp(self):
        """Create a temporary workspace directory before each test."""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary workspace directory after each test."""
        shutil.rmtree(self.test_dir)

    def test_cli_init_command(self):
        """Verify 'dw_agent init' creates required input and output subdirectories."""
        sys.argv = ["dw_agent", "init", "--project", self.test_dir]
        exit_code = main()
        self.assertEqual(exit_code, 0)
        self.assertTrue((Path(self.test_dir) / "inputs" / "requirements").exists())
        self.assertTrue((Path(self.test_dir) / "output").exists())

    def test_cli_explain_command(self):
        """Verify 'dw_agent explain' prints explanations for artifacts and rule IDs."""
        sys.argv = ["dw_agent", "explain", "--artifact", "bus-matrix"]
        exit_code = main()
        self.assertEqual(exit_code, 0)

        sys.argv = ["dw_agent", "explain", "--artifact", "GRAIN-001"]
        exit_code = main()
        self.assertEqual(exit_code, 0)

    def test_cli_demo_command(self):
        """Verify end-to-end design pipeline on a seeded demo project."""
        demo_dir = tempfile.mkdtemp()
        try:
            from scripts.seed_demo import seed_demo_project
            seed_demo_project(demo_dir, "ecommerce")
            sys.argv = ["dw_agent", "design", "--project", demo_dir, "--dialect", "sqlite"]
            exit_code = main()
            self.assertEqual(exit_code, 0)
            self.assertTrue((Path(demo_dir) / "output" / "manifest.json").exists())
        finally:
            shutil.rmtree(demo_dir)

# Main script entrypoint for running unittest runner
if __name__ == "__main__":
    unittest.main()

