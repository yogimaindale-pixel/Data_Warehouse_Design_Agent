# Module docstring explaining project input file scanning and SHA-256 checksum calculation
"""Inventory scanner scanning project inputs directory and computing SHA-256 file hashes."""

# Import os module for directory navigation, path joining, and file size extraction
import os
# Import hashlib module for computing SHA-256 file hashes
import hashlib
# Import List type hinting primitive
from typing import List
# Import InputFile dataclass contract
from dw_agent.contracts import InputFile

# Function computing SHA-256 hex digest for a given input file
def calculate_file_hash(filepath: str) -> str:
    """Calculate the SHA-256 cryptographic hash digest of a file.

    Args:
        filepath (str): Absolute or relative filesystem path to the file.

    Returns:
        str: Hexadecimal SHA-256 digest string, or error indicator if unreadable.
    """
    # Create SHA-256 hash object
    sha256 = hashlib.sha256()
    try:
        # Open file in binary read mode
        with open(filepath, "rb") as f:
            # Read file in 64KB chunks to efficiently process large files without exhausting RAM
            for chunk in iter(lambda: f.read(65536), b""):
                sha256.update(chunk)
        # Return hex digest string
        return sha256.hexdigest()
    except Exception:
        # Fallback string if file cannot be read
        return "error_reading_file"

# Function recursively scanning the project's 'inputs/' folder
def scan_input_inventory(project_path: str) -> List[InputFile]:
    """Recursively scan project 'inputs/' directory and construct InputFile inventory records.

    Args:
        project_path (str): Path to root project folder.

    Returns:
        List[InputFile]: List of discovered input files with path, extension, hash, and byte size.
    """
    # Construct absolute path to inputs directory
    inputs_dir = os.path.join(project_path, "inputs")
    # Initialize empty inventory list
    inventory: List[InputFile] = []
    
    # Return empty inventory if inputs directory does not exist
    if not os.path.exists(inputs_dir):
        return inventory

    # Walk recursively through inputs folder subdirectories
    for root, _, files in os.walk(inputs_dir):
        for f in files:
            # Get full file path
            full_path = os.path.join(root, f)
            # Calculate relative path from project root
            rel_path = os.path.relpath(full_path, project_path)
            # Extract lowercase file extension without leading dot
            ext = os.path.splitext(f)[1].lower().strip(".")
            # Get file size in bytes
            size = os.path.getsize(full_path)
            # Compute SHA-256 file checksum
            file_hash = calculate_file_hash(full_path)
            # Append typed InputFile record
            inventory.append(
                InputFile(
                    file_path=rel_path,
                    file_type=ext,
                    file_hash=file_hash,
                    size_bytes=size
                )
            )
    return inventory

