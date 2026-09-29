# Module docstring explaining PII detection using regex pattern matching
"""Quality profiler identifying candidate Personally Identifiable Information (PII) columns from column naming patterns."""

# Import re module for regex pattern matching
import re
# Import List type hint
from typing import List

# Predefined list of regex patterns indicating sensitive PII attributes
PII_PATTERNS = [r"email", r"ssn", r"phone", r"credit_card", r"password", r"first_name", r"last_name", r"address", r"dob", r"tax_id"]

# Function scanning column names against PII regex patterns
def detect_pii_candidates(column_names: List[str]) -> List[str]:
    """Detect PII candidate columns by matching column names against known PII regex patterns.

    Args:
        column_names (List[str]): List of column names to evaluate.

    Returns:
        List[str]: Sublist of column names flagged as PII candidates.
    """
    pii = []
    for c in column_names:
        if any(re.search(pat, c, re.IGNORECASE) for pat in PII_PATTERNS):
            pii.append(c)
    return pii

