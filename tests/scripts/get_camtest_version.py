"""
This script runs a function from an external package that is installed at a different location.

The purpose of this script is to check that the PYTHONPATH or sys.path are properly set.
"""

from camtest.version import get_git_version
from rich import print

print(f"CAMTEST git version = [bold default]{get_git_version()}[/]")
