"""Unit tests for DDL Generator across supported SQL dialects."""

import unittest
from dw_agent.contracts import DimensionSpec, DimensionColumn, FactSpec, FactMeasure
from dw_agent.generation.ddl_generator import generate_target_ddl

class TestDDLGenerator(unittest.TestCase):
    def setUp(self):
        self.dim = DimensionSpec(
            table_name="dim_customer",
            grain="One row per customer profile state",
            surrogate_key="customer_sk",
            business_key="customer_bk",
            is_scd2=True,
            columns=[
                DimensionColumn(name="customer_bk", data_type="VARCHAR(64)", scd_type=1),
                DimensionColumn(name="email", data_type="VARCHAR(100)", scd_type=2),
                DimensionColumn(name="effective_date", data_type="TIMESTAMP", scd_type=2),
                DimensionColumn(name="expiration_date", data_type="TIMESTAMP", scd_type=2),
                DimensionColumn(name="is_current", data_type="BOOLEAN", scd_type=2)
            ]
        )
        self.fact = FactSpec(
            table_name="fact_sales",
            process_id="BP-001",
            grain_sentence="One row per sales line item",
            fact_type="transaction",
            foreign_keys=[{"col": "customer_sk", "target_dim": "dim_customer"}],
            degenerate_dimensions=["order_id"],
            measures=[FactMeasure(name="sales_amount", formula="SUM(sales_amount)", source_column="sales_amount", additivity="additive")]
        )

    def test_generate_sqlite_ddl(self):
        target_sql, rollback_sql = generate_target_ddl([self.dim], [self.fact], "sqlite")
        self.assertIn("CREATE TABLE dim_customer", target_sql)
        self.assertIn("INTEGER PRIMARY KEY", target_sql)
        self.assertIn("INSERT OR IGNORE INTO dim_customer", target_sql)
        self.assertIn("CREATE VIEW v_dim_customer_current", target_sql)
        self.assertIn("DROP VIEW IF EXISTS v_dim_customer_current", rollback_sql)

    def test_generate_postgresql_ddl(self):
        target_sql, rollback_sql = generate_target_ddl([self.dim], [self.fact], "postgresql")
        self.assertIn("BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY", target_sql)
        self.assertIn("CONSTRAINT fk_fact_sales_dim_customer", target_sql)
        self.assertIn("DROP TABLE IF EXISTS fact_sales;", rollback_sql)

    def test_generate_snowflake_ddl(self):
        target_sql, rollback_sql = generate_target_ddl([self.dim], [self.fact], "snowflake")
        self.assertIn("NUMBER(38,0) IDENTITY(1,1) PRIMARY KEY", target_sql)
        self.assertIn("CREATE VIEW v_dim_customer_current", target_sql)

    def test_generate_bigquery_ddl(self):
        target_sql, rollback_sql = generate_target_ddl([self.dim], [self.fact], "bigquery")
        self.assertIn("INT64", target_sql)
        self.assertIn("STRING", target_sql)
        self.assertIn("CURRENT_TIMESTAMP()", target_sql)
        self.assertIn("CREATE OR REPLACE VIEW v_dim_customer_current", target_sql)

    def test_generate_synapse_ddl(self):
        target_sql, rollback_sql = generate_target_ddl([self.dim], [self.fact], "synapse")
        self.assertIn("INT IDENTITY(1,1) PRIMARY KEY", target_sql)
        self.assertIn("CONSTRAINT fk_fact_sales_dim_customer", target_sql)

if __name__ == "__main__":
    unittest.main()

