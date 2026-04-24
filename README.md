# Germany Job Search Pipeline

A Python-based data pipeline that aggregates, filters, and outputs relevant job opportunities for students seeking internships or entry-level roles in Germany.

---

## Overview

This project automatically collects job postings from multiple APIs and filters them based on:

- Location (Tübingen area or remote)
- Relevant technical keywords (Python, AI, Software, etc.)
- Student-friendly roles (internships, working student, junior)

The final result is a clean, deduplicated dataset of relevant job offers in `.csv` format, ready for quick review and application.

---

## Features

- Multi-source aggregation  
  - Arbeitnow API  
  - Remotive API  

- Data normalization  
  - Standardizes job fields across APIs (title, company, location, etc.)

- Smart filtering  
  - Keeps only:
    - Jobs in selected cities (e.g. Tübingen, Stuttgart)
    - OR fully remote positions
    - AND relevant technical roles

- Duplicate removal  
  - Ensures clean output without repeated postings

- Structured output  
  - Exports filtered jobs into a ready-to-use CSV file

---

## Filtering Logic

A job is considered relevant if:

- It contains at least one **target keyword**, such as:
  - `python`, `software`, `developer`, `machine learning`, `ai`, `intern`, `werkstudent`

AND

- It satisfies one of the following:
  - Located in a **target city** (e.g. Tübingen, Stuttgart)
  - Marked as **remote** or **hybrid**

This ensures that only realistic and accessible opportunities are kept.

---

## How to Run

git clone https://github.com/your-username/germany-job-search-pipeline.git
cd germany-job-search-pipeline
pip install -r requirements.txt
python main.py
data/processed/filtered_jobs.csv
