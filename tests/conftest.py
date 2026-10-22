import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "agent"))

# Set default AWS env vars for tests
os.environ.setdefault("AWS_REGION", "ap-southeast-1")
os.environ.setdefault("AWS_DEFAULT_REGION", "ap-southeast-1")
os.environ.setdefault("TABLE_NAME", "test-table")
os.environ.setdefault("BUCKET", "test-bucket")
