"""Integration test for end-to-end DW Design Agent pipeline."""

import unittest
import tempfile
import os
import shutil
from scripts.seed_demo import seed_demo_project
from dw_agent.cli import run_design_pipeline

class TestPipelineIntegration(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        seed_demo_project(self.test_dir, "ecommerce")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_end_to_end_ecommerce(self):
        res = run_design_pipeline(self.test_dir, "sqlite")
        self.assertTrue(res["is_accepted"])
        self.assertEqual(res["deliverables_count"], 27)
        
        output_files = os.listdir(os.path.join(self.test_dir, "output"))
        self.assertIn("00_EXECUTIVE_SUMMARY.md", output_files)
        self.assertIn("13_TARGET_DDL.sql", output_files)
        self.assertIn("manifest.json", output_files)

if __name__ == "__main__":
    unittest.main()
