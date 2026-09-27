"""Quality profiling for data nulls, distributions, min/max, PII candidates."""

import re
from typing import List, Dict, Any

PII_PATTERNS = [r"email", r"ssn", r"phone", r"credit_card", r"password", r"first_name", r"last_name", r"address", r"dob", r"tax_id"]

def detect_pii_candidates(column_names: List[str]) -> List[str]:
    pii = []
    for c in column_names:
        if any(re.search(pat, c, re.IGNORECASE) for pat in PII_PATTERNS):
            pii.append(c)
    return pii
