import sys
import os
from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def create_project_root() -> None:
    root = os.path.join(os.path.dirname(get_project_root()), 'FastAPI_REF')
    sys.path.append(root)
