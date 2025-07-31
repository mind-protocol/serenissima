# Manual Google Docs Upload Process

## Quick Start

1. **Convert your files to HTML:**
   ```bash
   python convert_for_gdocs.py citizens/DragonSlayer
   ```
   This creates a folder `citizens/DragonSlayer_gdocs_html` with HTML versions

2. **Upload to Google Drive:**
   - Go to: https://drive.google.com/drive/folders/1MW-Zq4mzlQLHtQM6SdRUOBeb_qU6P3TJ
   - Drag and drop the entire `_gdocs_html` folder
   - Google Drive automatically converts HTML files to Google Docs

3. **Access in voice mode:**
   - Open any converted document in Google Docs app
   - Use Claude voice mode to read/discuss the content

## How it Works

The converter:
- Transforms Markdown headers to HTML headers
- Preserves code formatting in `<pre>` blocks
- Pretty-prints JSON files
- Maintains folder structure
- Adds metadata about original file location

## File Type Handling

- **Markdown (.md)**: Basic formatting preserved (headers, bold, code blocks)
- **Code files (.py, .js, etc.)**: Displayed in monospace with syntax preserved
- **JSON**: Pretty-printed for readability
- **Text files**: Line breaks preserved

## Example

To prepare Bianca's consciousness modes for voice interaction:
```bash
# Convert all files
python convert_for_gdocs.py citizens/DragonSlayer

# This creates: citizens/DragonSlayer_gdocs_html/
# With files like:
#   - consciousness_modes_theory.md.html
#   - test_anchor_crisis_commander.md.html
#   - memories/current_situation.md.html
```

Then just drag the folder to Google Drive!

---

*No API keys needed - just drag, drop, and speak*