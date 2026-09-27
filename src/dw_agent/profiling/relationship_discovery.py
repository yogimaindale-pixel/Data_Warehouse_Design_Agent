"""Relationship discovery across sample tables."""

from typing import List, Dict, Any

def discover_candidate_relationships(tables_profile: Dict[str, Any]) -> List[Dict[str, str]]:
    relationships = []
    # Match columns with same name across tables that end with _id or _key
    table_names = list(tables_profile.keys())
    for i in range(len(table_names)):
        for j in range(i + 1, len(table_names)):
            t1, t2 = table_names[i], table_names[j]
            cols1 = tables_profile[t1].get("columns", {})
            cols2 = tables_profile[t2].get("columns", {})
            
            for c1 in cols1:
                if c1 in cols2 and (c1.endswith("_id") or c1.endswith("_key") or c1.endswith("_code")):
                    relationships.append({
                        "table_1": t1,
                        "col_1": c1,
                        "table_2": t2,
                        "col_2": c1
                    })
    return relationships
