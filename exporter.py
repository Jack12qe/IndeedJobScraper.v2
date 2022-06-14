import csv


def save_to_csv(jobs):
    with open("indeed_jobs.csv", "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["title", "company", "income", "location", "link"])
        for job in jobs:
            writer.writerow(list(job.values()))
