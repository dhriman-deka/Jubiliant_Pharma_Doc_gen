# Jubilant Pharmova Website Scraper

A simple yet powerful web scraper for [Jubilant Pharmova](https://www.jubilantpharmova.com/) built with Crawl4AI.

## Overview

This scraper crawls the Jubilant Pharmova website to extract content in both Markdown and HTML formats. It's designed to be easy to use while providing comprehensive data extraction.

## Features

- **Single Domain Crawling**: Focuses only on the jubilantpharmova.com domain
- **Configurable Page Limits**: Default limit of 50 pages to manage resource usage
- **Multiple Format Support**: Extracts content in both Markdown and HTML
- **Automatic Timestamping**: Output files include timestamps for easy tracking
- **JSON Output**: Data is saved in structured JSON format for easy processing

## Requirements

- Python 3.7+
- crawl4ai (version 0.5.0+)
- asyncio
- json

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd <repository-folder>/scraper
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the scraper with:

```bash
python jubilant_simple_scraper.py
```

The script will:
1. Connect to the Jubilant Pharmova website
2. Crawl up to 50 pages within the domain
3. Extract content in Markdown and HTML formats
4. Save results to a JSON file with timestamp (e.g., `jubilant_pharmova_data_20250321_120000.json`)

## Configuration

You can modify the following parameters in `jubilant_simple_scraper.py`:

```python
# Change the maximum number of pages to crawl
max_pages=50  

# Include external domains (set to True if needed)
include_external=False

# Add other parameters supported by Crawl4AI
```

## Output Format

The output JSON file contains an array of objects with the following structure:

```json
[
  {
    "url": "https://www.jubilantpharmova.com/page-url",
    "content": "Markdown content of the page",
    "html": "HTML content of the page"
  },
  ...
]
```

## Limitations

- The scraper respects robots.txt by default
- Crawling is limited to 50 pages to avoid overwhelming the server
- Only internal links within jubilantpharmova.com are followed

## Legal Considerations

This scraper is for educational purposes. Please ensure you comply with Jubilant Pharmova's terms of service and robots.txt policy when using this tool.

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 