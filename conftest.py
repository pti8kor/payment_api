# Root-level conftest.py
# Ensures the project root is on sys.path so 'payments_api' is importable
# during pytest runs both locally and in CI.
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
