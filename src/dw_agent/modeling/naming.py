# Module docstring explaining warehouse naming conventions and snake_case formatting
"""Naming standards enforcer guaranteeing consistent snake_case, table prefixes (dim_, fact_), surrogate key suffixes (_sk), and natural key suffixes (_bk)."""

# Import re module for regex identifier formatting
import re

# Helper function converting arbitrary string identifiers to snake_case
def to_snake_case(name: str) -> str:
    """Convert PascalCase, camelCase, or space-separated names to lower snake_case.

    Args:
        name (str): Identifier string to convert.

    Returns:
        str: Sanitized snake_case identifier string.
    """
    s = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
    s = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s).lower()
    return re.sub(r'[\s\-]+', '_', s)

# Formatter guaranteeing 'fact_' prefix on fact table names
def format_fact_table_name(base_name: str, prefix: str = "fact_") -> str:
    clean = to_snake_case(base_name)
    if clean.startswith("fact_"):
        return clean
    return f"{prefix}{clean}"

# Formatter guaranteeing 'dim_' prefix on dimension table names
def format_dim_table_name(base_name: str, prefix: str = "dim_") -> str:
    clean = to_snake_case(base_name)
    if clean.startswith("dim_"):
        return clean
    return f"{prefix}{clean}"

# Formatter constructing surrogate key names with '_sk' suffix
def format_surrogate_key(table_name: str, suffix: str = "_sk") -> str:
    clean = to_snake_case(table_name)
    if clean.startswith("dim_"):
        clean = clean[4:]
    elif clean.startswith("fact_"):
        clean = clean[5:]
    return f"{clean}{suffix}"

# Formatter constructing durable business key names with '_bk' suffix
def format_business_key(table_name: str, base_key: str = "id", suffix: str = "_bk") -> str:
    clean_tbl = to_snake_case(table_name)
    if clean_tbl.startswith("dim_"):
        clean_tbl = clean_tbl[4:]
    return f"{clean_tbl}_{suffix.strip('_')}"

