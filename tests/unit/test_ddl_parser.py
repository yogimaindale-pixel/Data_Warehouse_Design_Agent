"""Unit tests for DDL Parser."""

import unittest
from dw_agent.discovery.ddl_parser import parse_source_ddl

class TestDDLParser(unittest.TestCase):
    def test_parse_sample_ddl(self):
        # Smoke test DDL parser with empty/missing folder
        tables = parse_source_ddl("/tmp/non_existent_folder")
        self.assertEqual(len(tables), 0)

if __name__ == "__main__":
    unittest.main()
