# OpenFDA Downloader

A Python application for downloading large datasets from the **OpenFDA API** using cursor-based pagination.

The downloader is designed to retrieve complete datasets efficiently and reliably while producing page-based JSON files that can be imported directly into Excel using Power Query.

---

## Features

- Cursor-based pagination using the OpenFDA `Link` header
- Automatic API key support
- Automatic retry with exponential backoff
- Graceful shutdown (Ctrl+C)
- Logging to both console and file
- Download manifest
- One JSON file per API page
- Configurable page size (up to 1000 records)
- Configurable development limit (`max_pages`)
- Clean separation between downloading and Excel analysis

---

## Project Structure

```
OpenFDADownloader/
│
├── config/
│   └── settings.json
│
├── logs/
│
├── output/
│   ├── manifest.json
│   └── pages/
│       ├── page_000001.json
│       ├── page_000002.json
│       └── ...
│
├── src/
│   ├── api.py
│   ├── config.py
│   ├── downloader.py
│   ├── file_utils.py
│   ├── logger.py
│   ├── manifest.py
│   └── page_writer.py
│
├── main.py
├── requirements.txt
└── README.md
```

---

# Requirements

- Python 3.12+
- OpenFDA API Key
- Internet connection

---

# Installation

Clone the repository:

```bash
git clone https://github.com/<your_username>/OpenFDADownloader.git

cd OpenFDADownloader
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

---

# Configuration

Create a `.env` file in the project root.

```
OPENFDA_API_KEY=your_api_key_here
```

The API key can be requested from:

https://open.fda.gov/apis/authentication/

---

Edit:

```
config/settings.json
```

Example:

```json
{
    "endpoint": "device/event",
    "search": "search=date_received:[20130101 TO 20130131]",
    "sort": "date_received:asc",
    "page_size": 1000,
    "output_directory": "output",
    "retry_count": 3,
    "retry_delay": 2,
    "timeout": 30,
    "max_pages": 5
}
```
max_pages can be used for testing (0 = download all)


---

# Running

```bash
python main.py
```

---

# Output

Each API page is written as an individual JSON file.

```
output/
│
├── manifest.json
│
└── pages/
    ├── page_000001.json
    ├── page_000002.json
    ├── page_000003.json
    └── ...
```

The downloader automatically removes previously downloaded page files before starting a new download.

---

# Manifest

After a successful download a `manifest.json` file is created.

Example:

```json
{
    "endpoint": "device/event",
    "search": "...",
    "page_size": 1000,
    "pages_downloaded": 125,
    "records_downloaded": 125000,
    "download_started": "...",
    "download_finished": "...",
    "duration_seconds": 215
}
```

---

# Logging

Logs are written to:

```
logs/pipeline.log
```

The log records:

- download start
- configuration
- downloaded pages
- interruptions
- errors
- summary

---

# Excel Integration

The downloader is designed to work together with **Power Query**.

Instead of importing one very large JSON file, Power Query imports all JSON files from:

```
output/pages/
```

and combines them into a single dataset for further transformation.

This keeps downloads reliable while allowing Excel to work with OpenFDA datasets.

---

# Current Status

Current functionality includes:

- Downloading OpenFDA data
- Cursor pagination
- Automatic retries
- Logging
- Manifest generation
- Page-based output
- Graceful shutdown

Future improvements include:

- Resume interrupted downloads
- Additional statistics
- Incremental updates
- Support for additional OpenFDA endpoints

---

# License

This project is released under the MIT License.

---

# Acknowledgements

Data is provided by the U.S. Food and Drug Administration (FDA) through the OpenFDA API.

https://open.fda.gov/