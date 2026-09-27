"""Metadata loader for CSV/JSON/YAML source metadata."""

import os
import csv
import json
import yaml
from typing import Dict, Any, List

def load_source_metadata(project_path: str) -> Dict[str, Any]:
    meta_dir = os.path.join(project_path, "inputs", "source_metadata")
    metadata: Dict[str, Any] = {"tables": {}, "mappings": []}

    if not os.path.exists(meta_dir):
        return metadata

    for fname in os.listdir(meta_dir):
        fpath = os.path.join(meta_dir, fname)
        if fname.endswith(".json"):
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    metadata["tables"].update(data.get("tables", {}))
        elif fname.endswith(".yaml") or fname.endswith(".yml"):
            with open(fpath, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
                if isinstance(data, dict):
                    metadata["tables"].update(data.get("tables", {}))
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
