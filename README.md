# Wuzzuf Job Scraper (API-based)

A Python script that scrapes job listings from Wuzzuf by reverse-engineering
their internal API.

## Features
- API-based scraping
- Pagination support
- Company extraction
- HTML cleaning
- Description truncation
- CSV, Excel outputs

- 
## Extracted Job Fields

The scraper collects the following data for each job listing:

Job title 
Job city 
Job country 
Company name 
Career level (Entry, Experienced, Manager, etc.) 
Employment type (Full Time, Part Time, Remote, etc.) 
Job posting date 
Job expiration date 
Cleaned job description text 
Cleaned job requirements (if available)
Job-related keywords
Original Wuzzuf job URL 
External application URL (if available) 

## Technologies
- Python
- Requests
- Pandas
- BeautifulSoup
- openpyxl
## Usage
```bash
pip install -r requirements.txt
python scraper.py
