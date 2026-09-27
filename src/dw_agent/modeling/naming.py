"""Naming standards enforcer."""

import re

def to_snake_case(name: str) -> str:
    s = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
    s = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s).lower()
    return re.sub(r'[\s\-]+', '_', s)

def format_fact_table_name(base_name: str, prefix: str = "fact_") -> str:
    clean = to_snake_case(base_name)
    if clean.startswith("fact_"):
        return clean
    return f"{prefix}{clean}"

def format_dim_table_name(base_name: str, prefix: str = "dim_") -> str:
    clean = to_snake_case(base_name)
    if clean.startswith("dim_"):
        return clean
    return f"{prefix}{clean}"

def format_surrogate_key(table_name: str, suffix: str = "_sk") -> str:
    clean = to_snake_case(table_name)
    if clean.startswith("dim_"):
        clean = clean[4:]
    elif clean.startswith("fact_"):
        clean = clean[5:]
    return f"{clean}{suffix}"

def format_business_key(table_name: str, base_key: str = "id", suffix: str = "_bk") -> str:
    clean_tbl = to_snake_case(table_name)
    if clean_tbl.startswith("dim_"):
        clean_tbl = clean_tbl[4:]
    return f"{clean_tbl}_{suffix.strip('_')}"
