# Module docstring explaining business requirements and KPI parsing from input files
"""Requirement parser extracting KPIs, business questions, and security specifications from Markdown and CSV files."""

# Import os module for path operations and directory listing
import os
# Import re module for regex pattern matching across text lines
import re
# Import csv module for reading KPI inventory CSV files
import csv
# Import List type hint
from typing import List
# Import Requirement dataclass contract
from dw_agent.contracts import Requirement

# Main requirement parser function reading input requirement folders
def parse_requirements(project_path: str) -> List[Requirement]:
    """Parse business requirements and KPI definitions from 'inputs/requirements/' and 'inputs/kpi_inventory/'.

    Args:
        project_path (str): Path to root project folder.

    Returns:
        List[Requirement]: List of parsed Requirement objects.
    """
    req_dir = os.path.join(project_path, "inputs", "requirements")
    kpi_dir = os.path.join(project_path, "inputs", "kpi_inventory")
    requirements: List[Requirement] = []
    
    # 1. Parse Markdown/TXT requirement specification documents
    if os.path.exists(req_dir):
        for fname in os.listdir(req_dir):
            fpath = os.path.join(req_dir, fname)
            if not os.path.isfile(fpath):
                continue
            rel_path = os.path.relpath(fpath, project_path)
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            # Parse headers and bullet points
            lines = content.splitlines()
            current_req_id = 1
            for line in lines:
                line_str = line.strip()
                # Match bullet lists ('- ', '* ') or numbered items ('1. ')
                if line_str.startswith("- ") or line_str.startswith("* ") or re.match(r"^\d+\.", line_str):
                    clean_text = re.sub(r"^[-*\d.]+\s*", "", line_str)
                    cat = "KPI"
                    # Classify category based on keywords
                    if "security" in clean_text.lower() or "pii" in clean_text.lower():
                        cat = "Security"
                    elif "history" in clean_text.lower() or "scd" in clean_text.lower():
                        cat = "History"
                    elif "refresh" in clean_text.lower() or "daily" in clean_text.lower():
                        cat = "Refresh"
                    
                    requirements.append(
                        Requirement(
                            req_id=f"REQ-{fname[:4].upper()}-{current_req_id:03d}",
                            title=clean_text[:60],
                            description=clean_text,
                            source_file=rel_path,
                            category=cat
                        )
                    )
                    current_req_id += 1

    # 2. Parse structured KPI CSV inventory files
    if os.path.exists(kpi_dir):
        for fname in os.listdir(kpi_dir):
            if fname.endswith(".csv"):
                fpath = os.path.join(kpi_dir, fname)
                rel_path = os.path.relpath(fpath, project_path)
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    reader = csv.DictReader(f)
                    req_idx = 1
                    for row in reader:
                        kpi_name = row.get("kpi_name") or row.get("name") or row.get("kpi") or f"KPI-{req_idx}"
                        desc = row.get("description") or row.get("formula") or kpi_name
                        requirements.append(
                            Requirement(
                                req_id=f"KPI-{req_idx:03d}",
                                title=f"KPI: {kpi_name}",
                                description=desc,
                                source_file=rel_path,
                                category="KPI"
                            )
                        )
                        req_idx += 1

    # 3. Fallback default requirement if no requirement files were provided
    if not requirements:
        requirements.append(
            Requirement(
                req_id="REQ-GEN-001",
                title="Default Analytical Reporting Requirement",
                description="Provide dimensional analytical model for order and transaction insights.",
                source_file="inputs/requirements/default.md",
                category="KPI"
            )
        )

    return requirements

