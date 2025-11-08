# config.py
from pathlib import Path
import os

# Define project root (assuming config.py is in the project root)
PROJECT_ROOT = Path(__file__).resolve().parent

# Define shared directories
GENERATED_FILES_DIR = PROJECT_ROOT / "generated_files"
GENERATED_FILES_DIR.mkdir(parents=True, exist_ok=True)

# Export as string for compatibility with os.path operations
GENERATED_FILES_DIR_STR = str(GENERATED_FILES_DIR)
