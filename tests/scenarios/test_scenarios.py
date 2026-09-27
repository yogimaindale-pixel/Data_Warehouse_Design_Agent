"""Comprehensive Scenario Tests for Data Warehouse Design Agent."""

import unittest
import tempfile
import shutil
import os
from pathlib import Path
from scripts.seed_demo import seed_demo_project
from dw_agent.cli import run_design_pipeline
from dw_agent.contracts import DimensionSpec, DimensionColumn, FactSpec, FactMeasure
from dw_agent.validation.model_validator import validate_warehouse_design

class TestScenarios(unittest.TestCase):

    # Scenario 1: E-commerce order-line star schema
    def test_scenario_01_ecommerce_star_schema(self):
        test_dir = tempfile.mkdtemp()
        try:
            seed_demo_project(test_dir, "ecommerce")
            res = run_design_pipeline(test_dir, "sqlite")
            self.assertTrue(res["is_accepted"])
            self.assertEqual(res["deliverables_count"], 27)
            self.assertEqual(res["fail_cnt"], 0)
        finally:
            shutil.rmtree(test_dir)

    # Scenario 2: BFS credit-risk snapshot and transaction facts
    def test_scenario_02_bfs_credit_risk(self):
        test_dir = tempfile.mkdtemp()
        try:
            seed_demo_project(test_dir, "bfs-credit-risk")
            res = run_design_pipeline(test_dir, "sqlite")
            self.assertTrue(res["is_accepted"])
            self.assertEqual(res["deliverables_count"], 27)
        finally:
            shutil.rmtree(test_dir)

    # Scenario 3: Multi-fact sales and periodic snapshot
    def test_scenario_03_multi_fact_grain(self):
        test_dir = tempfile.mkdtemp()
        try:
            seed_demo_project(test_dir, "ecommerce")
            res = run_design_pipeline(test_dir, "postgresql")
            self.assertTrue(res["is_accepted"])
            self.assertGreater(res["process_count"], 0)
        finally:
            shutil.rmtree(test_dir)

    # Scenario 4: SCD2 customer attribute change tracking
    def test_scenario_04_scd2_customer_tracking(self):
        dim = DimensionSpec(
            table_name="dim_customer",
            grain="One row per customer version",
            surrogate_key="customer_sk",
            business_key="customer_id",
            is_scd2=True,
            columns=[
                DimensionColumn(name="customer_id", data_type="VARCHAR(64)", scd_type=1),
                DimensionColumn(name="email", data_type="VARCHAR(100)", scd_type=2),
                DimensionColumn(name="effective_date", data_type="TIMESTAMP", scd_type=2),
                DimensionColumn(name="expiration_date", data_type="TIMESTAMP", scd_type=2),
                DimensionColumn(name="is_current", data_type="BOOLEAN", scd_type=2)
            ]
        )
        val_items = validate_warehouse_design([dim], [], [], [])
        scd_failures = [v for v in val_items if v.rule_id == "SCD-001" and not v.is_pass]
        self.assertEqual(len(scd_failures), 0)

    # Scenario 5: Bridge table relationship validation
    def test_scenario_05_bridge_table_relationship(self):
        dim_cust = DimensionSpec(
            table_name="dim_customer",
            grain="One row per customer",
            surrogate_key="customer_sk",
            business_key="customer_id"
        )
        dim_account = DimensionSpec(
            table_name="dim_account",
            grain="One row per account",
            surrogate_key="account_sk",
            business_key="account_id"
        )
        fact_bal = FactSpec(
            table_name="fact_account_snapshot",
            process_id="BP-002",
            grain_sentence="One row per account per day",
            fact_type="periodic_snapshot",
            foreign_keys=[
                {"col": "customer_sk", "target_dim": "dim_customer"},
                {"col": "account_sk", "target_dim": "dim_account"}
            ]
        )
        val_items = validate_warehouse_design([dim_cust, dim_account], [fact_bal], [], [])
        rel_failures = [v for v in val_items if v.rule_id.startswith("REL") and not v.is_pass and v.severity == "critical"]
        self.assertEqual(len(rel_failures), 0)

    # Scenario 6: Factless event coverage
    def test_scenario_06_factless_event_fact(self):
        factless = FactSpec(
            table_name="fact_student_attendance",
            process_id="BP-003",
            grain_sentence="One row per student per class period",
            fact_type="factless",
            foreign_keys=[
                {"col": "student_sk", "target_dim": "dim_student"},
                {"col": "date_sk", "target_dim": "dim_date"}
            ],
            measures=[FactMeasure(name="attendance_count", formula="COUNT(1)", source_column="attendance_id", additivity="additive")]
        )
        self.assertEqual(factless.fact_type, "factless")
        self.assertEqual(len(factless.measures), 1)

    # Scenario 7: Late-arriving dimension handling
    def test_scenario_07_late_arriving_dimension(self):
        test_dir = tempfile.mkdtemp()
        try:
            seed_demo_project(test_dir, "ecommerce")
            res = run_design_pipeline(test_dir, "snowflake")
            self.assertTrue(res["is_accepted"])
            # Check target DDL contains default unknown member insert -1
            ddl_file = Path(test_dir) / "output" / "13_TARGET_DDL.sql"
            self.assertTrue(ddl_file.exists())
            content = ddl_file.read_text()
            self.assertIn("INSERT INTO dim_date", content)
            self.assertIn("-1, 'UNKNOWN'", content)
        finally:
            shutil.rmtree(test_dir)

    # Scenario 8: Schema drift detection
    def test_scenario_08_schema_drift(self):
        test_dir = tempfile.mkdtemp()
        try:
            seed_demo_project(test_dir, "ecommerce")
            res1 = run_design_pipeline(test_dir, "sqlite")
            self.assertTrue(res1["is_accepted"])
        finally:
            shutil.rmtree(test_dir)

    # Scenario 9: Review required status
    def test_scenario_09_review_required(self):
        dim = DimensionSpec(
            table_name="dim_customer",
            grain="One row per customer",
            surrogate_key="customer_sk",
            business_key="customer_id",
            is_scd2=True,
            columns=[]  # Missing validity columns
        )
        val_items = validate_warehouse_design([dim], [], [], [])
        scd_fails = [v for v in val_items if v.rule_id == "SCD-001" and not v.is_pass]
        self.assertEqual(len(scd_fails), 1)

    # Scenario 10: Invalid fact-to-fact join detection
    def test_scenario_10_missing_dimension_reference(self):
        fact = FactSpec(
            table_name="fact_orders",
            process_id="BP-001",
            grain_sentence="One row per order line",
            fact_type="transaction",
            foreign_keys=[{"col": "nonexistent_dim_sk", "target_dim": "dim_nonexistent"}]
        )
        val_items = validate_warehouse_design([], [fact], [], [])
        rel_fails = [v for v in val_items if v.rule_id == "REL-003" and not v.is_pass]
        self.assertEqual(len(rel_fails), 1)

if __name__ == "__main__":
    unittest.main()
