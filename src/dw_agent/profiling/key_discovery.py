"""Candidate key discovery from profiled column stats."""

from typing import List, Dict, Any

def discover_candidate_keys(col_stats: Dict[str, Dict[str, Any]], total_rows: int) -> List[str]:
    candidates = []
    if total_rows == 0:
        return candidates

    for col_name, stats in col_stats.items():
        distinct_cnt = stats.get("distinct_count", 0)
        null_cnt = stats.get("null_count", 0)
        
        # 100% uniqueness ratio and 0 nulls -> natural key candidate
        if null_cnt == 0 and distinct_cnt == total_rows:
            candidates.append(col_name)
        elif col_name.lower().endswith("_id") or col_name.lower().endswith("_code") or col_name.lower() == "id":
            if null_cnt == 0 and (distinct_cnt / total_rows) > 0.9:
                candidates.append(col_name)

    return candidates
