"""Model validation report markdown writer."""

from typing import List
from dw_agent.contracts import ValidationItem

def generate_validation_report(validation_items: List[ValidationItem]) -> str:
    lines = []
    lines.append("# Model Validation & Quality Gate Report\n")
    lines.append("| Rule ID | Category | Severity | Status | Action | Message |")
    lines.append("|---|---|---|---|---|---|")
    
    for v in validation_items:
        status_str = "PASS" if v.is_pass else "FAIL"
        lines.append(f"| {v.rule_id} | {v.category} | {v.severity} | `{status_str}` | {v.action} | {v.message} |")

    return "\n".join(lines)
