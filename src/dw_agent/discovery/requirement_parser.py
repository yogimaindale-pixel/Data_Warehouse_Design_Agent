"""Requirement parser for extracting KPIs, questions, dimensions, and security requirements."""

import os
import re
import csv
from typing import List
from dw_agent.contracts import Requirement

def parse_requirements(project_path: str) -> List[Requirement]:
    req_dir = os.path.join(project_path, "inputs", "requirements")
    kpi_dir = os.path.join(project_path, "inputs", "kpi_inventory")
    requirements: List[Requirement] = []
    
    # Parse Markdown/TXT requirements
    if os.path.exists(req_dir):
        for fname in os.listdir(req_dir):
            fpath = os.path.join(req_dir, fname)
            if not os.path.isfile(fpath):
                continue
            rel_path = os.path.relpath(fpath, project_path)
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            # Simple header / bullet parser
            lines = content.splitlines()
            current_req_id = 1
            for line in lines:
                line_str = line.strip()
                if line_str.startswith("- ") or line_str.startswith("* ") or re.match(r"^\d+\.", line_str):
                    clean_text = re.sub(r"^[-*\d.]+\s*", "", line_str)
                    cat = "KPI"
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

    # Parse KPI CSV inventory
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

    if not requirements:
        # Default fallback requirement if folder was empty
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
