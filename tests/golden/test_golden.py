"""Golden tests verifying deterministic output deliverable structure."""

import unittest
import tempfile
import shutil
from pathlib import Path
from scripts.seed_demo import seed_demo_project
from dw_agent.cli import run_design_pipeline

class TestGolden(unittest.TestCase):
    def test_golden_deliverables_output_structure(self):
        test_dir = tempfile.mkdtemp()
        try:
            seed_demo_project(test_dir, "ecommerce")
            res = run_design_pipeline(test_dir, "sqlite")
            out_dir = Path(test_dir) / "output"
            
            expected_deliverables = [
                "00_EXECUTIVE_SUMMARY.md",
                "01_INPUT_INVENTORY.csv",
                "02_REQUIREMENTS_CATALOG.csv",
                "03_OPEN_QUESTIONS_AND_ASSUMPTIONS.md",
                "04_SOURCE_PROFILE.xlsx",
                "05_BUSINESS_PROCESS_CATALOG.csv",
                "06_GRAIN_DECLARATIONS.md",
                "07_BUS_MATRIX.csv",
                "08_DIMENSION_CATALOG.xlsx",
                "09_FACT_CATALOG.xlsx",
                "10_CONCEPTUAL_MODEL.mmd",
                "11_LOGICAL_MODEL.mmd",
                "12_PHYSICAL_MODEL.mmd",
                "13_TARGET_DDL.sql",
                "14_ROLLBACK_DDL.sql",
                "15_STTM.xlsx",
                "16_ETL_SPECIFICATIONS.md",
                "17_DATA_QUALITY_RULES.xlsx",
                "18_LINEAGE.csv",
                "19_SECURITY_AND_PRIVACY_CONSIDERATIONS.md",
                "20_PERFORMANCE_DESIGN.md",
                "21_TEST_CASES.xlsx",
                "22_REQUIREMENTS_TRACEABILITY_MATRIX.xlsx",
                "23_ARCHITECTURE_DECISIONS.md",
                "24_MODEL_VALIDATION_REPORT.md",
                "25_IMPLEMENTATION_BACKLOG.csv",
                "26_REVIEW_CHECKLIST.md",
                "manifest.json"
            ]

            for fname in expected_deliverables:
                fpath = out_dir / fname
                self.assertTrue(fpath.exists(), f"Missing golden deliverable file: {fname}")
                self.assertGreater(fpath.stat().st_size, 0, f"Golden deliverable file is empty: {fname}")

            # Verify manifest
            import json
            manifest_data = json.loads((out_dir / "manifest.json").read_text())
            self.assertEqual(manifest_data["deliverables_count"], 27)
            self.assertTrue(manifest_data["is_accepted"])
        finally:
            shutil.rmtree(test_dir)

if __name__ == "__main__":
    unittest.main()
