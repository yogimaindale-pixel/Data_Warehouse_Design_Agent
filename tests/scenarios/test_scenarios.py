"""Scenario tests for e-commerce and BFS credit-risk."""

import unittest
import tempfile
import shutil
from scripts.seed_demo import seed_demo_project
from dw_agent.cli import run_design_pipeline

class TestScenarios(unittest.TestCase):
    def test_bfs_credit_risk_scenario(self):
        test_dir = tempfile.mkdtemp()
        try:
            seed_demo_project(test_dir, "bfs-credit-risk")
            res = run_design_pipeline(test_dir, "sqlite")
            self.assertTrue(res["is_accepted"])
            self.assertGreater(res["process_count"], 0)
        finally:
            shutil.rmtree(test_dir)

if __name__ == "__main__":
    unittest.main()
