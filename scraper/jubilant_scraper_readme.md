# Jubilant Pharmova Website Scraper

A simple web scraper for the Jubilant Pharmova website using Crawl4AI.

## Features

- Crawls the Jubilant Pharmova website (https://www.jubilantpharmova.com/)
- Collects page content in Markdown format
- Saves results as structured JSON
- Configurable depth and page limits

## Setup

1. Install requirements:

```bash
pip install -r requirements.txt
```

2. Run the scraper:

```bash
python jubilant_scraper.py
```

## Configuration

The scraper is configured with:
- Breadth-First Search (BFS) crawling strategy
- Max depth of 2 levels from homepage
- Limited to 50 pages
- Only follows internal links within jubilantpharmova.com
- Extracts content in Markdown format

You can adjust these parameters in the script to suit your needs. 