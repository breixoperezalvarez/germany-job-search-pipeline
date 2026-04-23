from fetch_jobs import fetch_arbeitnow_jobs, fetch_remotive_jobs
from filter_jobs import combine_jobs, filter_jobs
from save_jobs import save_raw_json, save_csv

def main() -> None:
    arbeitnow_output = "data/raw/arbeitnow_jobs.json"
    remotive_output = "data/raw/remotive_jobs.json"
    filtered_output = "data/processed/filtered_jobs.csv"

    print("Fetching jobs from Arbeitnow...")
    arbeitnow_data = fetch_arbeitnow_jobs()

    print("Fetching jobs from Remotive...")
    remotive_data = fetch_remotive_jobs()

    print("Saving raw API responses...")
    save_raw_json(arbeitnow_data, arbeitnow_output)
    save_raw_json(remotive_data, remotive_output)

    print("Combining jobs from both sources...")
    all_jobs_df = combine_jobs(arbeitnow_data, remotive_data)

    print("Filtering jobs for relevant roles...")
    filtered_jobs_df = filter_jobs(all_jobs_df)

    print("Saving filtered jobs...")
    save_csv(filtered_jobs_df, filtered_output)

    print("\nProcess completed")
    print(f"Total jobs collected: {len(all_jobs_df)}")
    print(f"Relevant jobs after filtering: {len(filtered_jobs_df)}")
    print(f"Filtered jobs saved to: {filtered_output}")

if __name__ == "__main__":
    main()