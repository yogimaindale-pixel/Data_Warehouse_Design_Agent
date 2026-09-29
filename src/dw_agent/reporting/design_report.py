# Module docstring explaining quality gate validation markdown report generation
"""Model validation report markdown writer formatting validation items into a structured Markdown table."""

# Import List type hint
from typing import List
# Import ValidationItem contract dataclass
from dw_agent.contracts import ValidationItem

# Function generating validation report markdown table string
def generate_validation_report(validation_items: List[ValidationItem]) -> str:
    """Format validation items list into a clean GitHub Flavored Markdown table.

    Args:
        validation_items (List[ValidationItem]): List of validation gate result items.

    Returns:
        str: Markdown document string.
    """
    lines = []
    lines.append("# Model Validation & Quality Gate Report\n")
    lines.append("| Rule ID | Category | Severity | Status | Action | Message |")
    lines.append("|---|---|---|---|---|---|")
    
    for v in validation_items:
        status_str = "PASS" if v.is_pass else "FAIL"
        lines.append(f"| {v.rule_id} | {v.category} | {v.severity} | `{status_str}` | {v.action} | {v.message} |")

    return "\n".join(lines)

