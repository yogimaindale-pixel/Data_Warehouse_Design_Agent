# Module docstring explaining loading source metadata catalogs from JSON, YAML, or CSV formats
"""Metadata loader parsing source catalog definitions from JSON, YAML, and CSV files in 'inputs/source_metadata/'."""

# Import os module for file traversal and path joining
import os
# Import csv module for reading CSV catalog metadata
import csv
# Import json module for parsing JSON catalog metadata
import json
# Import PyYAML safe_load for parsing YAML catalog metadata
import yaml
# Import type hints
from typing import Dict, Any, List

# Function parsing source metadata files from inputs/source_metadata/
def load_source_metadata(project_path: str) -> Dict[str, Any]:
    """Load source catalog metadata from JSON, YAML, or CSV files in 'inputs/source_metadata/'.

    Args:
        project_path (str): Root project folder path.

    Returns:
        Dict[str, Any]: Dictionary containing parsed table and column metadata maps.
    """
    meta_dir = os.path.join(project_path, "inputs", "source_metadata")
    metadata: Dict[str, Any] = {"tables": {}, "mappings": []}

    # Return empty dictionary if directory is missing
    if not os.path.exists(meta_dir):
        return metadata

    # Read each file in metadata folder
    for fname in os.listdir(meta_dir):
        fpath = os.path.join(meta_dir, fname)
        # Parse JSON metadata
        if fname.endswith(".json"):
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    metadata["tables"].update(data.get("tables", {}))
        # Parse YAML / YML metadata
        elif fname.endswith(".yaml") or fname.endswith(".yml"):
            with open(fpath, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
                if isinstance(data, dict):
                    metadata["tables"].update(data.get("tables", {}))
        # Parse CSV metadata
        elif fname.endswith(".csv"):
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    tbl = row.get("table_name") or row.get("source_table")
                    if tbl:
                        if tbl not in metadata["tables"]:
                            metadata["tables"][tbl] = {"columns": []}
                        metadata["tables"][tbl]["columns"].append(row)

    return metadata

