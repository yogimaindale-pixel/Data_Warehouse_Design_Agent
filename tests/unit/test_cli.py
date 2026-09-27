"""Unit tests for dw_agent CLI subcommands."""

import unittest
import tempfile
import shutil
import sys
from pathlib import Path
from dw_agent.cli import main

class TestCLI(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_cli_init_command(self):
        sys.argv = ["dw_agent", "init", "--project", self.test_dir]
        exit_code = main()
        self.assertEqual(exit_code, 0)
        self.assertTrue((Path(self.test_dir) / "inputs" / "requirements").exists())
        self.assertTrue((Path(self.test_dir) / "output").exists())

    def test_cli_explain_command(self):
        sys.argv = ["dw_agent", "explain", "--artifact", "bus-matrix"]
        exit_code = main()
        self.assertEqual(exit_code, 0)

        sys.argv = ["dw_agent", "explain", "--artifact", "GRAIN-001"]
        exit_code = main()
        self.assertEqual(exit_code, 0)

    def test_cli_demo_command(self):
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

if __name__ == "__main__":
    unittest.main()
