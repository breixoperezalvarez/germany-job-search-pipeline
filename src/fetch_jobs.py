import json
import os
from typing import Any

import requests

ARBEITNOW_URL = "https://www.arbeitnow.com/api/job-board-api"
REMOTIVE_URL = "https://remotive.com/api/remote-jobs"

def fetch_json(url: str) -> dict[str, Any]:
    """Fetch JSON dadta from an API endpoint"""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            "AppleWebKit/537.36 (KHTML, like Gecko)"
            "Chrome/124.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()

def fetch_arbeitnow_jobs() -> dict[str, Any]:
    """Fetch Germany-focused jobs from the Arbeitnow API"""
    return fetch_json(ARBEITNOW_URL)

def fetch_remotive_jobs() -> dict[str, Any]:
    """Fetch remote jobs from the Remotive API"""
    return fetch_json(REMOTIVE_URL)

def save_raw_json(data: dict[str, Any], output_path: str) -> None:
    """Save raw API response to a JSON file"""
    os.makedirs(os.path.dirname(output_path), exists_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)