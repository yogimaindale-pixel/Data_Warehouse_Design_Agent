# Module docstring explaining Mermaid diagram text generation for ER modeling
"""Mermaid diagram generator producing conceptual, logical, and physical Entity-Relationship (ER) model diagrams."""

# Import List and Tuple type hints
from typing import List, Tuple
# Import contract dataclasses
from dw_agent.contracts import DimensionSpec, FactSpec

# Function generating conceptual, logical, and physical Mermaid ER diagram strings
def generate_mermaid_models(dimensions: List[DimensionSpec], facts: List[FactSpec]) -> Tuple[str, str, str]:
    """Generate conceptual, logical, and physical Mermaid.js erDiagram markup strings.

    Args:
        dimensions (List[DimensionSpec]): Dimension specifications.
        facts (List[FactSpec]): Fact specifications.

    Returns:
        Tuple[str, str, str]: Tuple of (conceptual_mermaid_string, logical_mermaid_string, physical_mermaid_string).
    """
    # 1. Conceptual Model (High-level entity relationship connections)
    conceptual = []
    conceptual.append("erDiagram")
    for f in facts:
        for fk in f.foreign_keys:
            conceptual.append(f"    {f.table_name.upper()} }}|--|| {fk['target_dim'].upper()} : \"references\"")

    # 2. Logical Model (Entity attributes, PK/FK declarations, business keys)
    logical = []
    logical.append("erDiagram")
    for d in dimensions:
        logical.append(f"    {d.table_name.upper()} {{")
        logical.append(f"        string {d.surrogate_key} PK")
        logical.append(f"        string {d.business_key} BK")
        for c in d.columns:
            logical.append(f"        string {c.name}")
        logical.append("    }")
    for f in facts:
        logical.append(f"    {f.table_name.upper()} {{")
        for fk in f.foreign_keys:
            logical.append(f"        string {fk['col']} FK")
        for m in f.measures:
            logical.append(f"        number {m.name}")
        logical.append("    }")
        for fk in f.foreign_keys:
            logical.append(f"    {f.table_name.upper()} }}|--|| {fk['target_dim'].upper()} : \"has\"")

    # 3. Physical Model (Exact SQL data types, surrogate keys, table constraints)
    physical = []
    physical.append("erDiagram")
    for d in dimensions:
        physical.append(f"    {d.table_name} {{")
        physical.append(f"        INTEGER {d.surrogate_key} PK")
        physical.append(f"        VARCHAR {d.business_key}")
        for c in d.columns:
            physical.append(f"        {c.data_type} {c.name}")
        physical.append("    }")
    for f in facts:
        physical.append(f"    {f.table_name} {{")
        physical.append(f"        INTEGER {f.table_name}_id PK")
        for fk in f.foreign_keys:
            physical.append(f"        INTEGER {fk['col']} FK")
        for m in f.measures:
            physical.append(f"        NUMERIC {m.name}")
        physical.append("    }")
        for fk in f.foreign_keys:
            physical.append(f"    {f.table_name} }}|--|| {fk['target_dim']} : \"FK\"")

    return "\n".join(conceptual), "\n".join(logical), "\n".join(physical)

