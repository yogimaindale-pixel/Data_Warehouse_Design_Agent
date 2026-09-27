"""Unit tests for DDL Generator."""

import unittest
from dw_agent.contracts import DimensionSpec, DimensionColumn
from dw_agent.generation.ddl_generator import generate_target_ddl

class TestDDLGenerator(unittest.TestCase):
    def test_generate_sqlite_ddl(self):
        dim = DimensionSpec(
            table_name="dim_customer",
            grain="One row per customer",
            surrogate_key="customer_sk",
            business_key="customer_bk",
            columns=[DimensionColumn(name="email", data_type="VARCHAR(100)")]
        )
        target_sql, rollback_sql = generate_target_ddl([dim], [], "sqlite")
        self.assertIn("CREATE TABLE dim_customer", target_sql)
        self.assertIn("DROP TABLE IF EXISTS dim_customer", rollback_sql)

if __name__ == "__main__":
    unittest.main()
