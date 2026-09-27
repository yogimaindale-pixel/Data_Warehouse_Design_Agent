"""Acceptance criteria evaluator."""

from typing import List
from dw_agent.contracts import ValidationItem

def evaluate_acceptance(validation_items: List[ValidationItem]) -> Tuple[bool, int, int, int]:
    pass_cnt = sum(1 for v in validation_items if v.is_pass)
    warn_cnt = sum(1 for v in validation_items if not v.is_pass and v.severity == "warning")
    fail_cnt = sum(1 for v in validation_items if not v.is_pass and v.severity == "critical")
    
    is_accepted = fail_cnt == 0
    return is_accepted, pass_cnt, warn_cnt, fail_cnt
