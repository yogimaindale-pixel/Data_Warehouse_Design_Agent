# Module docstring explaining natural key discovery rules based on profiled column metrics
"""Candidate key discovery module identifying potential natural keys from column uniqueness and naming patterns."""

# Import List, Dict, and Any type hint primitives
from typing import List, Dict, Any

# Function discovering unique candidate key columns
def discover_candidate_keys(col_stats: Dict[str, Dict[str, Any]], total_rows: int) -> List[str]:
    """Identify candidate natural keys based on 100% uniqueness or _id/_code suffix conventions.

    Args:
        col_stats (Dict[str, Dict[str, Any]]): Column profiling statistics dictionary.
        total_rows (int): Total rows in sample dataset.

    Returns:
        List[str]: List of column names identified as candidate natural keys.
    """
    candidates = []
    # Return empty list if total_rows is zero
    if total_rows == 0:
        return candidates

    # Evaluate each column against key criteria
    for col_name, stats in col_stats.items():
        distinct_cnt = stats.get("distinct_count", 0)
        null_cnt = stats.get("null_count", 0)
        
        # Rule 1: 100% uniqueness ratio and 0 nulls -> definite natural key candidate
        if null_cnt == 0 and distinct_cnt == total_rows:
            candidates.append(col_name)
        # Rule 2: Ends with _id or _code or is named 'id' with >90% uniqueness and 0 nulls
        elif col_name.lower().endswith("_id") or col_name.lower().endswith("_code") or col_name.lower() == "id":
            if null_cnt == 0 and (distinct_cnt / total_rows) > 0.9:
                candidates.append(col_name)

    return candidates

