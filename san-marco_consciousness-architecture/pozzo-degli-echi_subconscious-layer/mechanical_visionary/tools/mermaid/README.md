# Mermaid Diagram to Image Converter

A proper tool to convert mermaid diagrams in markdown files to PNG images using the official mermaid CLI.

## Requirements

- Python 3
- @mermaid-js/mermaid-cli (npm package)

## Installation

Install the official mermaid CLI:
```bash
sudo npm install -g @mermaid-js/mermaid-cli
```

## Usage

```bash
python mermaid_cli_converter.py <markdown_file>
```

Example:
```bash
python mermaid_cli_converter.py ../../HOOK_ARCHITECTURE_DIAGRAM.md
```

This will:
1. Find all mermaid code blocks in the markdown file
2. Create PNG images with the same base name using the official mermaid CLI
3. If multiple diagrams exist, they'll be numbered: `file.diagram_1.png`, `file.diagram_2.png`, etc.

## How it Works

1. Extracts mermaid diagram code from markdown
2. Creates temporary `.mmd` files
3. Uses `mmdc` (mermaid CLI) to generate properly sized PNG images
4. Saves as PNG next to the original markdown file

No browser screenshots, no cropping, no hacks - just the official tool doing what it's designed to do.

## Future Integration

This tool will be integrated into the Living Memory Cascade documentation system, automatically converting diagrams when documentation is updated.