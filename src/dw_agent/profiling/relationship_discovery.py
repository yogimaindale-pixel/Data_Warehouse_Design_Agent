# Module docstring explaining cross-table key relationship discovery
"""Relationship discovery module detecting candidate primary key to foreign key join paths across tables."""

# Import List, Dict, and Any type hint primitives
from typing import List, Dict, Any

# Function discovering candidate relationships based on matching column names
def discover_candidate_relationships(tables_profile: Dict[str, Any]) -> List[Dict[str, str]]:
    """Discover candidate join relationships by identifying common key column names across tables.

    Args:
        tables_profile (Dict[str, Any]): Dictionary mapping table names to their profiled column metadata.

    Returns:
        List[Dict[str, str]]: List of relationship dictionaries [{table_1, col_1, table_2, col_2}].
    """
    relationships = []
    # Extract all profiled table names
    table_names = list(tables_profile.keys())
    
    # Compare every pair of tables
    for i in range(len(table_names)):
        for j in range(i + 1, len(table_names)):
            t1, t2 = table_names[i], table_names[j]
            cols1 = tables_profile[t1].get("columns", {})
            cols2 = tables_profile[t2].get("columns", {})
            
            # Check for shared column names ending with _id, _key, or _code
            for c1 in cols1:
                if c1 in cols2 and (c1.endswith("_id") or c1.endswith("_key") or c1.endswith("_code")):
                    relationships.append({
                        "table_1": t1,
                        "col_1": c1,
                        "table_2": t2,
                        "col_2": c1
                    })
    return relationships

