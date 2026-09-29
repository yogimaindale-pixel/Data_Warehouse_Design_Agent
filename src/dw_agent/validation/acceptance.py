# Module docstring explaining acceptance criteria evaluation
"""Acceptance criteria evaluator calculating PASS, WARNING, and CRITICAL validation totals to determine overall design acceptance."""

# Import List and Tuple type hints
from typing import List, Tuple
# Import ValidationItem dataclass contract
from dw_agent.contracts import ValidationItem

# Evaluator function summarizing validation status counts
def evaluate_acceptance(validation_items: List[ValidationItem]) -> Tuple[bool, int, int, int]:
    """Evaluate overall warehouse design acceptance based on validation severity levels.

    Args:
        validation_items (List[ValidationItem]): List of validation result items.

    Returns:
        Tuple[bool, int, int, int]: Tuple of (is_accepted_bool, pass_count, warning_count, critical_fail_count).
    """
    pass_cnt = sum(1 for v in validation_items if v.is_pass)
    warn_cnt = sum(1 for v in validation_items if not v.is_pass and v.severity == "warning")
    fail_cnt = sum(1 for v in validation_items if not v.is_pass and v.severity == "critical")
    
    # Model is accepted only if critical_fail_count == 0
    is_accepted = fail_cnt == 0
    return is_accepted, pass_cnt, warn_cnt, fail_cnt

