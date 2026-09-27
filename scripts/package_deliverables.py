"""Zip packaging script for deliverables."""

import os
import sys
import shutil

def package_deliverables(project_path: str = "."):
    out_dir = os.path.join(project_path, "output")
    if not os.path.exists(out_dir):
        print(f"Error: {out_dir} does not exist.")
        sys.exit(1)

    archive_name = os.path.join(project_path, "dw_design_deliverables")
    shutil.make_archive(archive_name, "zip", out_dir)
    print(f"Deliverables successfully packaged to {archive_name}.zip")

if __name__ == "__main__":
    proj = sys.argv[1] if len(sys.argv) > 1 else "."
    package_deliverables(proj)
