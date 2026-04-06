# Wuzzuf Job Scraper

> A powerful Python-based job scraper that extracts job listings from Wuzzuf using their internal API. Ideal for data analysis, job market research, and building job databases.

## 🎯 Overview

This project reverse-engineers Wuzzuf's internal API to efficiently scrape job listings. It handles pagination, batch processing, and robust error handling to collect detailed job information and export it to multiple formats (CSV and Excel).

**Note**: This scraper is intended for educational and research purposes only.

---

## ✨ Features

- **API-Based Scraping**: Leverages Wuzzuf's internal API for reliable and efficient data extraction
- **Pagination Support**: Configurable multi-page scraping with automatic pagination handling
- **Batch Processing**: Fetches job details in optimized batches to improve performance
- **HTML Cleaning**: Automatically removes HTML tags from descriptions and requirements
- **Structured Data**: Extracts and organizes 13+ job fields per listing
- **Multiple Exports**: Save results in both CSV and Excel formats
- **Error Handling**: Comprehensive logging and graceful error management
- **Configurable Delays**: Built-in rate limiting to respect server resources
- **Logging**: Detailed console and file-based logging for debugging and monitoring

---

## 📊 Extracted Job Fields

Each job listing includes:

| Field | Description |
|-------|-------------|
| **Title** | Job position title |
| **City** | Job location city |
| **Country** | Job location country |
| **Company** | Hiring company name |
| **Career Level** | Entry, Experienced, Manager, etc. |
| **Work Type** | Full Time, Part Time, Remote, Contract, etc. |
| **Posted At** | Job posting timestamp |
| **Expire At** | Job listing expiration date |
| **Description** | Cleaned job description (truncated) |
| **Requirements** | Cleaned job requirements (truncated) |
| **Keywords** | Relevant job keywords/skills |
| **Job URL** | Direct link to job on Wuzzuf |
| **Redirect URL** | External application URL (if available) |

---

## 🛠️ Technologies

- **Python 3.x**
- **Requests** - HTTP library for API calls
- **Pandas** - Data manipulation and CSV/Excel export
- **BeautifulSoup4** - HTML parsing and cleaning
- **openpyxl** - Excel file generation

---

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Internet connection

---

## 🚀 Installation

1. **Clone or download this repository**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install requests pandas beautifulsoup4 openpyxl
   ```

---

## 💻 Usage

### Basic Usage

Run the scraper with default settings (10 pages):
```bash
python scraper.py
```

### Custom Configuration

Modify the script parameters before running:

```python
if __name__ == "__main__":
    # Change max_pages to control how many pages to scrape
    scraper = WazzufScraper(max_pages=5)  # Scrape 5 pages instead of 10
    scraper.run()
```

### Configuration Options

Inside the `WazzufScraper` class `__init__` method:

```python
self.PAGE_SIZE = 15              # Jobs per API request (default: 15)
self.BATCH_SIZE = 10            # Jobs per detail fetch batch (default: 10)
self.DELAY = 0.5                # Seconds between requests (default: 0.5)
self.MAX_PAGES = max_pages      # Number of pages to scrape (default: 5)
self.MAX_DESC_LENGTH = 100      # Text truncation length (default: 100 chars)
```

---

## 📁 Output

The scraper creates an `output/` directory with:

- **csv_wuzzuf_jobs.csv** - Comma-separated values file (Excel compatible)
- **excel_wuzzuf_jobs.xlsx** - Native Excel workbook format

### Logs

Detailed logs are saved to:
- **log/scraper.log** - Full execution log file
- **Console output** - Real-time progress information

Example log output:
```
2026-04-06 10:15:32 - INFO - Starting to fetch job IDs...
2026-04-06 10:15:33 - INFO - Collected 15 job IDs (Page 1/10)
2026-04-06 10:15:35 - INFO - Fetched details for batch 1/2
2026-04-06 10:15:38 - INFO - All job details saved to CSV and Excel in output folder
```

---

## 📊 Output Example

The exported files contain rows like:

| Title | Company | City | Career Level | Work Type | Description |
|-------|---------|------|--------------|-----------|-------------|
| Senior Python Developer | Tech Corp | Cairo | Experienced | Full Time | We are looking for... |
| Junior Data Analyst | Analytics Inc | Giza | Entry | Full Time | Analyze and visualize... |

---

## ⚙️ How It Works

1. **Fetch Job IDs**: Makes API calls to `https://wuzzuf.net/api/search/job` to get job listings
2. **Extract Companies**: Parses company names from the search results
3. **Fetch Job Details**: Makes batch requests to get full job information
4. **Clean & Process**: 
   - Removes HTML tags using BeautifulSoup
   - Truncates long descriptions
   - Normalizes dates and text
5. **Export Data**: Saves processed data to CSV and Excel formats

---

## ⚠️ Important Notes

- **Rate Limiting**: The scraper includes built-in delays to avoid overwhelming the server
- **Ethical Use**: Respect Wuzzuf's terms of service and robots.txt
- **Large Datasets**: When scraping many pages, the script may take several minutes
- **API Changes**: If Wuzzuf's API structure changes, the scraper may need updates

---

## 🐛 Troubleshooting

### Common Issues

**"No Job IDs found"**
- Check your internet connection
- Verify Wuzzuf's website is accessible
- Try reducing `max_pages` for testing

**"Connection timeout"**
- Increase timeout values in the code
- Check your network speed
- Try again later if Wuzzuf's servers are slow

**"Empty output files"**
- Ensure job data was successfully fetched (check logs)
- Verify Wuzzuf's API hasn't changed structurally

### Viewing Logs

Check detailed execution logs:
```bash
cat log/scraper.log  # On Linux/Mac
type log/scraper.log  # On Windows
```

---

## 📝 Project Structure

```
Wazzuf Job Finder/
├── scraper.py              # Main scraper script
├── requirements.txt        # Project dependencies
├── README.md              # This file
├── sample_output.csv      # Example output
├── log/                   # Logging directory
│   └── scraper.log       # Execution logs
├── output/                # Results directory
│   ├── csv_wuzzuf_jobs.csv
│   └── excel_wuzzuf_jobs.xlsx
└── PreView/               # Preview/documentation
```

---

## 🔄 Future Enhancements

- [ ] Add filtering by job type, location, or keyword
- [ ] Implement caching to avoid re-scraping
- [ ] Add database export (SQLite, MySQL)
- [ ] Create web interface for easy configuration
- [ ] Add email notifications for new jobs
- [ ] Implement job deduplication

---

## 📄 License

This project is provided as-is for educational and research purposes.

---

## ⚡ Quick Tips

- Start with `max_pages=1` to test the setup
- Monitor `log/scraper.log` during execution
- Use Excel files for better formatting and charts
- Export regularly to build a job market database

---

*Last Updated: April 2026*
