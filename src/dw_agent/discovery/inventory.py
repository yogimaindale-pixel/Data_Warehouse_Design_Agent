"""Inventory scanner for scanning project inputs and calculating file hashes."""

import os
import hashlib
from typing import List
from dw_agent.contracts import InputFile

def calculate_file_hash(filepath: str) -> str:
    sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception:
        return "error_reading_file"

def scan_input_inventory(project_path: str) -> List[InputFile]:
    inputs_dir = os.path.join(project_path, "inputs")
    inventory: List[InputFile] = []
    
    if not os.path.exists(inputs_dir):
        return inventory

    for root, _, files in os.walk(inputs_dir):
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, project_path)
            ext = os.path.splitext(f)[1].lower().strip(".")
            size = os.path.getsize(full_path)
            file_hash = calculate_file_hash(full_path)
            inventory.append(
                InputFile(
                    file_path=rel_path,
                    file_type=ext,
                    file_hash=file_hash,
                    size_bytes=size
                )
            )
    return inventory
