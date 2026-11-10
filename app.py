from __future__ import annotations
import sys
from pathlib import Path
import runpy

app_path = Path(__file__).resolve().parent / "starter_v0" / "app.py"
if str(app_path.parent) not in sys.path:
    sys.path.insert(0, str(app_path.parent))

runpy.run_path(str(app_path), run_name="__main__")
