from typing import Any
import pandas as pd

TARGET_CITIES = [
    "tübingen",
    "stuttgart",
    "jena",
    "berlin",
    "munich",
    "münchen",
    "hamburg",
    "frankfurt",
    "cologne",
    "köln"
]

TARGET_KEYWORDS = [
    "python",
    "data",
    "analyst",
    "developer",
    "backend",
    "automation",
    "intern",
    "internship",
    "werkstudent",
    "working student",
    "junior",
    "machine learning",
    "ai",
    "software"
]

REMOTE_KEYWORDS = [
    "remote",
    "home office",
    "home-office",
    "hybrid"
]

def safe_lower(value: Any) -> str:
    """Convert a value to lowercase string safely"""
    if value is None:
        return ""
    return str(value).strip().lower()

def extract_arbeitnow_jobs(raw_data: dict[str, Any]) -> list[dict[str, Any]]:
    """Normalize Arbeitnow API jobs into a common structure"""
    jobs = []

    for job in raw_data.get("data", []):
        location = job.get("location")
        tags = job.get("tags", [])
        job_types = job.get("job_types", [])

        jobs.append(
            {
                "source": "Arbeitnow",
                "title": job.get("title"),
                "company": job.get("company_name"),
                "location": location,
                "remote": job.get("remote"),
                "tags": ", ".join(tags) if isinstance(tags, list) else str(tags),
                "job_type": ", ".join(job_types) if isinstance(job_types, list) else str(job_types),
                "description": job.get("description"),
                "url": job.get("url")
            }
        )
    return jobs

def extract_remotive_jobs(raw_data: dict[str, Any]) -> list[dict[str, Any]]:
    """Normalize Remotive API jobs into a common structure"""
    jobs = []

    for job in raw_data.get("jobs", []):
        jobs.append(
            {
                "source": "Remotive",
                "title": job.get("title"),
                "company": job.get("company_name"),
                "location": job.get("candidate_required_location"),
                "remote": True,
                "tags": ", ".join(job.get("tags", [])),
                "job_type": job.get("job_type"),
                "description": job.get("description"),
                "url": job.get("url")
            }
        )
    return jobs

def combine_jobs(arbeitnow_data: dict[str, Any], remotive_data: dict[str, Any]) -> pd.DataFrame:
    """Combine normalized jobs from both APIs into one DataFrame"""
    arbeitnow_jobs = extract_arbeitnow_jobs(arbeitnow_data)
    remotive_jobs = extract_remotive_jobs(remotive_data)

    combined_jobs = arbeitnow_jobs + remotive_jobs
    return pd.DataFrame(combined_jobs)

def is_relevant_job(row: pd.Series) -> bool:
    """Check if a job matches my target search criteria"""
    title = safe_lower(row.get("title"))
    company = safe_lower(row.get("company"))
    location = safe_lower(row.get("location"))
    tags = safe_lower(row.get("tags"))
    job_type = safe_lower(row.get("job_type"))
    description = safe_lower(row.get("description"))
    remote = row.get("remote")

    combined_text = " ".join([title, company, location, tags, job_type, description])

    has_target_keyword = any(keyword in combined_text for keyword in TARGET_KEYWORDS)

    matches_city = any(city in location for city in TARGET_CITIES)
    matches_remote = bool(remote) or any(keyword in location for keyword in REMOTE_KEYWORDS)

    location_ok = matches_city or matches_remote

    return has_target_keyword and location_ok

def filter_jobs(df: pd.DataFrame) -> pd.DataFrame:
    """Filter DataFrame to relevant jobs and remove duplicates"""
    if df.empty:
        return df

    filtered_df = df[df.apply(is_relevant_job, axis=1)].copy()

    filtered_df = filtered_df.drop_duplicates(subset=["title", "company", "url"])

    filtered_df = filtered_df.sort_values(by=["source", "company", "title"], na_position="last")

    return filtered_df