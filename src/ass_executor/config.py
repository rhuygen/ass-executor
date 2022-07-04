from __future__ import annotations

from pathlib import Path

import yaml
from rich import print


def load_config(filename: Path | str):
    """Load the YAML config file from the given filename."""
    filename = Path(filename)

    with filename.open(mode='r') as fd:
        config = yaml.safe_load(fd)

    print(config)
    return config
