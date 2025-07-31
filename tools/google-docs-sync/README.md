# Google Docs Sync Tool

This tool uploads local folders to Google Drive and converts text files to Google Docs for voice interaction preparation.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Google Cloud credentials:**
   - Create a service account in Google Cloud Console
   - Download the JSON credentials file
   - Either:
     - Set environment variable: `export GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json`
     - Or pass the path as second argument to the script

3. **Important Note about API Keys:**
   - Google Drive API requires OAuth2 service account credentials
   - A simple API key (GOOGLE_API_KEY) is not sufficient for Drive operations
   - You need a service account JSON file with Drive API permissions

## Usage

```bash
# With environment variable set
python sync_to_gdocs.py /path/to/local/folder

# With explicit credentials path
python sync_to_gdocs.py /path/to/local/folder /path/to/credentials.json
```

## Example

To sync Bianca's consciousness modes for voice interaction:
```bash
python sync_to_gdocs.py ../../citizens/DragonSlayer
```

## Features

- Converts text files (.md, .txt, .json, .py, etc.) to Google Docs
- Preserves folder structure in Google Drive
- Creates timestamped root folder for each sync
- Skips hidden files and __pycache__ directories
- Shows progress and results summary

## Supported File Types

The following extensions are converted to Google Docs:
- `.md` (Markdown)
- `.txt` (Plain text)
- `.json` (JSON)
- `.py` (Python)
- `.js`, `.jsx` (JavaScript)
- `.ts`, `.tsx` (TypeScript)
- `.html`, `.css` (Web files)
- `.yml`, `.yaml` (YAML)
- `.sh`, `.bash` (Shell scripts)
- `.xml` (XML)
- `.csv` (CSV)
- `.log` (Log files)

## Target Folder

Files are uploaded to: https://drive.google.com/drive/folders/1MW-Zq4mzlQLHtQM6SdRUOBeb_qU6P3TJ

---

*Created for voice-to-voice interaction between NLR and Venice consciousness*