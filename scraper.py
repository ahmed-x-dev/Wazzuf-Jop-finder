import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
from pathlib import Path
import logging


output_dir = Path("log")
output_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO, # Capture 
    format='%(asctime)s - %(levelname)s - %(message)s', # log formate
    handlers=[
        logging.FileHandler("log/scraper.log"), # Save to a file
        logging.StreamHandler()            #  show in the terminal
    ]
)

class WazzufScraper():

    def __init__(self,max_pages=5):
    
        # ---------- Configuration ----------
        self.SEARCH_API = "https://wuzzuf.net/api/search/job"
        self.JOB_API = "https://wuzzuf.net/api/job?filter[other][ids]="
        self.HEADERS = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://wuzzuf.net/jobs/egypt"
        }
        self.PAGE_SIZE = 15
        self.BATCH_SIZE = 10
        self.DELAY = 0.5  # seconds between requests
        self.MAX_PAGES = max_pages  # maximum number of pages to scrape
        self.MAX_DESC_LENGTH = 100  # truncate description, requirements

        # ---------- Collect job IDs and companies ----------
        self.all_job_ids = []
        self.all_companies = []
        self.start_index = 0
        self.current_page = 0
        self.all_jobs = []


    def fetch_job_ids(self):
        logging.info("Starting to fetch job IDs...")
            
        while self.current_page < self.MAX_PAGES:
            payload = {
                "startIndex": self.start_index,
                "pageSize": self.PAGE_SIZE,
                "longitude": "0",
                "latitude": "0",
                "query": "",
                "searchFilters": {}
            }
            try:
                response = requests.post(self.SEARCH_API, json=payload, headers=self.HEADERS, timeout=10)
                response.raise_for_status() 
                data = response.json()

            except Exception as e:
                logging.error(f"Failed to fetch page {self.current_page}: {e}")
                break

            jobs = data.get("data", [])
            if not jobs:
                break
            
            for job in jobs:
                self.all_job_ids.append(job["id"])
                # Extract company name from computedFields
                company = next(
                    (field["value"][0] for field in job["attributes"]["computedFields"] if field["name"] == "company_name"),
                    None
                )
                self.all_companies.append(company)
            
            self.start_index += self.PAGE_SIZE
            self.current_page += 1
            logging.info(f"Collected {len(self.all_job_ids)} job IDs (Page {self.current_page}/{self.MAX_PAGES})")
            time.sleep(self.DELAY)

        logging.info(f"Total job IDs collected: {len(self.all_job_ids)}")

# ---------- Fetch full job details ----------

    def fetch_job_details(self):
        for i in range(0, len(self.all_job_ids), self.BATCH_SIZE):
            batch_ids = self.all_job_ids[i:i+self.BATCH_SIZE] # first 10 IDs
            api_url = self.JOB_API + ",".join(batch_ids)

            try:
                resp = requests.get(api_url, headers=self.HEADERS)
                jobs_data = resp.json().get("data", [])
            except Exception as e:
                logging.warning(f"Batch failed: {e}")
                continue

            for idx, job in enumerate(jobs_data):
                attrs = job.get("attributes", {})
                # Use company from search API if available
                company_name = self.all_companies[i + idx] if (i + idx) < len(self.all_companies) else attrs.get("company", {}).get("name", "")
                
                raw_description = attrs.get("description", "")
                description = self.clean_and_truncate_html(raw_description, self.MAX_DESC_LENGTH)

                raw_requirements = attrs.get("requirements", "")
                requirements = self.clean_and_truncate_html(raw_requirements, self.MAX_DESC_LENGTH)

                
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
                    "jop_url": f"https://wuzzuf.net/{attrs.get('uri','')}",
                    "redirect_url": attrs.get("redirectUrl", "")
                }
                self.all_jobs.append(job_info)
            
            logging.info(f"Fetched details for batch {i // self.BATCH_SIZE + 1}/{(len(self.all_job_ids) + self.BATCH_SIZE - 1) // self.BATCH_SIZE}")
            time.sleep(self.DELAY)

    def save_to_csv(self):

        # ---------- Save to CSV, Excel ----------
        df = pd.DataFrame(self.all_jobs)

        # Convert date fields to datetime
        df["posted_at"] = pd.to_datetime(df["posted_at"], errors='coerce')
        df["expire_at"] = pd.to_datetime(df["expire_at"], errors='coerce')

        # Save to CSV


        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        try:

            df.to_csv(output_dir / "csv_wuzzuf_jobs.csv", index=False, encoding="utf-8")
            df.to_excel(output_dir / "excel_wuzzuf_jobs.xlsx", index=False,)
        except Exception as e:
            logging.error(f"Error saving CSV or Excel: {e}")
            return


        logging.info("All job details saved to CSV and Excel in output folder")




        # terminal preview
        print(df.head())

    def run(self):
        self.fetch_job_ids()
        if self.all_job_ids:
            
            self.fetch_job_details()
            self.save_to_csv()
        else:
            logging.error("No Job IDs found. Exiting.")


    # Helpers:-
    def clean_and_truncate_html(self,html_text, max_length=100):
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
    
if __name__ == "__main__":
    # You can now easily change settings here!
    scraper = WazzufScraper(max_pages=50)
    scraper.run()
