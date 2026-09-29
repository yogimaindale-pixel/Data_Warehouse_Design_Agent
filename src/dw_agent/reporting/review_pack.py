# Module docstring explaining review checklist markdown generation
"""Review checklist generator creating architecture and governance sign-off criteria."""

# Function generating governance sign-off review checklist Markdown text
def generate_review_checklist() -> str:
    """Generate executive architectural sign-off checklist markdown text."""
    return """# Data Warehouse Design Review Checklist

## Architectural & Governance Sign-Off

- [ ] **Grain Validation**: Every fact table possesses a declared single-sentence grain rule.
- [ ] **Conformed Dimensions**: Dimension surrogate keys and business keys are conformed across all fact tables.
- [ ] **SCD Policy Approval**: Slowly Changing Dimension policies (Types 0, 1, 2, 3) match business history requirements.
- [ ] **Source-to-Target Mapping**: All target columns trace cleanly to source inputs or system defaults.
- [ ] **Data Quality Rules**: DQ threshold controls and quarantine actions are approved by governance.
- [ ] **Physical DDL Execution**: Target DDL parses and runs cleanly without syntax errors on target platform.
"""

