"""Small reusable project utilities."""

from pathlib import Path
import pandas as pd

def load_csv(path: str | Path) -> pd.DataFrame:
    """Load a CSV and keep path handling consistent across notebooks."""
    return pd.read_csv(Path(path))
