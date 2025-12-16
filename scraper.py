import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
from pathlib import Path

def clean_and_truncate_html(html_text, max_length=100):
    if not html_text:
        return ""
    
    # Remove HTML tags
    soup = BeautifulSoup(html_text, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    
    # Normalize spaces
    text = " ".join(text.split())
    
    # Truncate
    if len(text) > max_length:
        return text[:max_length] + "..."
    
    return text




# ---------- Configuration ----------
SEARCH_API = "https://wuzzuf.net/api/search/job"
JOB_API = "https://wuzzuf.net/api/job?filter[other][ids]="
HEADERS = {"User-Agent": "Mozilla/5.0"}
PAGE_SIZE = 15
BATCH_SIZE = 10
DELAY = 1  # seconds between requests
MAX_PAGES = 5  # maximum number of pages to scrape
MAX_DESC_LENGTH = 100  # truncate description

# ---------- Step 1: Collect job IDs and companies ----------
all_job_ids = []
all_companies = []
start_index = 0
current_page = 0

while current_page < MAX_PAGES:
    payload = {
        "startIndex": start_index,
        "pageSize": PAGE_SIZE,
        "longitude": "0",
        "latitude": "0",
        "query": "",
        "searchFilters": {}
    }
    
    response = requests.post(SEARCH_API, json=payload, headers=HEADERS)
    data = response.json()
    
    jobs = data.get("data", [])
    if not jobs:
        break
    
    for job in jobs:
        all_job_ids.append(job["id"])
        # Extract company name from computedFields
        company = next(
            (field["value"][0] for field in job["attributes"]["computedFields"] if field["name"] == "company_name"),
            None
        )
        all_companies.append(company)
    
    start_index += PAGE_SIZE
    current_page += 1
    print(f"Collected {len(all_job_ids)} job IDs (Page {current_page}/{MAX_PAGES})")
    time.sleep(DELAY)

print(f"Total job IDs collected: {len(all_job_ids)}")

# ---------- Step 2: Fetch full job details ----------
all_jobs = []

for i in range(0, len(all_job_ids), BATCH_SIZE):
    batch_ids = all_job_ids[i:i+BATCH_SIZE]
    api_url = JOB_API + ",".join(batch_ids)
    
    resp = requests.get(api_url, headers=HEADERS)
    jobs_data = resp.json().get("data", [])
    
    for idx, job in enumerate(jobs_data):
        attrs = job.get("attributes", {})
        # Use company from search API if available
        company_name = all_companies[i + idx] if (i + idx) < len(all_companies) else attrs.get("company", {}).get("name", "")
        
        raw_description = attrs.get("description", "")
        description = clean_and_truncate_html(raw_description, MAX_DESC_LENGTH)

        raw_requirements = attrs.get("requirements", "")
        requirements = clean_and_truncate_html(raw_requirements, MAX_DESC_LENGTH)

        
        job_info = {
            # "id": job.get("id", ""),
            "title": attrs.get("title", ""),
            "description": description,
            "requirements": requirements,
            "company": company_name,
            "city": attrs.get("location", {}).get("city", {}).get("name", ""),
            "country": attrs.get("location", {}).get("country", {}).get("name", ""),
            "keywords": ", ".join([kw.get("name", "") for kw in attrs.get("keywords", [])]),
            "career_level": attrs.get("careerLevel", {}).get("name", ""),
            "work_type": ", ".join([wt.get("displayedName", "") for wt in attrs.get("workTypes", [])]),
            "posted_at": attrs.get("postedAt", ""),
            "expire_at": attrs.get("expireAt", ""),
            "jop_url": f"https://wuzzuf.net/{attrs.get("uri","")}",
            "redirect_url": attrs.get("redirectUrl", "")
        }
        all_jobs.append(job_info)
    
    print(f"Fetched details for batch {i // BATCH_SIZE + 1}/{(len(all_job_ids) + BATCH_SIZE - 1) // BATCH_SIZE}")
    time.sleep(DELAY)

# ---------- Step 3: Save to pandas DataFrame ----------
df = pd.DataFrame(all_jobs)

# Convert date fields to datetime
df["posted_at"] = pd.to_datetime(df["posted_at"], errors='coerce')
df["expire_at"] = pd.to_datetime(df["expire_at"], errors='coerce')

# Save to CSV


output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

df.to_csv(output_dir / "wuzzuf_jobs.csv", index=False, encoding="utf-8")
print("All job details saved to output/wuzzuf_jobs.csv")


# Optional preview
print(df.head())
