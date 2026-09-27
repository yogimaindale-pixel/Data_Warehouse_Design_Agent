"""Unit tests for Grain Declaration."""

import unittest
from dw_agent.contracts import BusinessProcess
from dw_agent.modeling.grain import declare_grains

class TestGrain(unittest.TestCase):
    def test_declare_grain_transaction(self):
        bp = BusinessProcess(
            process_id="BP-001",
            name="Order Placement",
            triggering_event="Order line placed",
            proposed_fact_type="transaction",
            source_tables=["order_items"]
        )
        grains = declare_grains([bp], [], [])
        self.assertEqual(len(grains), 1)
        self.assertIn("order line item", grains[0].grain_sentence.lower())

if __name__ == "__main__":
    unittest.main()
