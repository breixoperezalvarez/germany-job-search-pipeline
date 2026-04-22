import json
import os
from typing import Any

import pandas as pd

def save_raw_json(data: dict[str, Any], output_path: str) -> None:
    """Save raw API response to a JSON file"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

def save_csv(df: pd.DataFrame, output_path: str) -> None:
    """Save a DataFrame to CSV"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
