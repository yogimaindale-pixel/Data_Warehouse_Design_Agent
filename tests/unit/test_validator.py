"""Unit tests for Model Validator."""

import unittest
from dw_agent.contracts import DimensionSpec, FactSpec, GrainDeclaration, ValidationItem
from dw_agent.validation.model_validator import validate_warehouse_design

class TestModelValidator(unittest.TestCase):
    def test_missing_grain_fails_validation(self):
        fact = FactSpec(
            table_name="fact_orders",
            process_id="BP-001",
            grain_sentence="",
            fact_type="transaction"
        )
        items = validate_warehouse_design([], [fact], [], [])
        criticals = [i for i in items if i.severity == "critical" and not i.is_pass]
        self.assertGreater(len(criticals), 0)

if __name__ == "__main__":
    unittest.main()
