# AnyFile to Markdown

Universal file to Markdown converter with PyQt6 GUI.

Converts **PDF, PPTX, DOCX, XLSX, images, HTML, CSV, JSON, XML, EPUB, ZIP, audio** and more to clean Markdown.

Powered by [MarkItDown](https://github.com/microsoft/markitdown) by Microsoft.

## Supported formats

| Category | Formats |
|---|---|
| Documents | PDF, DOCX, PPTX, XLSX, XLS |
| Images | JPEG, PNG, WebP, BMP, TIFF |
| Web | HTML, HTM |
| Data | CSV, JSON, XML |
| E-books | EPUB |
| Archives | ZIP |
| Audio | MP3, WAV |

## Features

- **Format auto-detection** by file extension
- **Dynamic options panel** — shows only relevant settings for the selected format
- **PDF engine choice**: MarkItDown (default) or PyMuPDF4LLM (advanced: DPI, table strategy, margins)
- **PPTX options**: slide range, notes, slide delimiters, image handling (disable / embed as base64 / LLM descriptions)
- **Image OCR/description** via LLM (requires OpenAI API key)
- **Background conversion** — UI stays responsive
- **Log window** + log file saved next to output

## Screenshots

<!-- Add screenshots here -->

## Installation

### Debian 13 (Trixie) / Ubuntu

```bash
sudo dpkg -i dist/anyfile-to-markdown_2.0.0-1_all.deb
sudo apt-get install -f -y
```

Package auto-installs `markitdown` from PyPI on first run.

### Windows 10

Download `AnyFileToMarkdown-Setup.exe` from Releases and run.

### macOS Tahoe 26

Download `AnyFileToMarkdown-macOS.dmg`, mount and drag to Applications.

### pip (any OS)

```bash
pip install anyfile-to-markdown
anyfile-to-markdown
```

### Run without install

```bash
python3 -m anyfile_to_markdown.app
```

## Usage

1. Click **Browse...** and select a file
2. Format is auto-detected; options panel updates
3. Adjust settings if needed
4. Click **Save as...** to choose output `.md`
5. Click **Convert**

Log appears in the window and is saved as `.md.log` next to output.

## Format-specific options

### PDF
| Option | Description |
|---|---|
| Pages | Page range: `1-5,7,10-N` |
| DPI | Rendering resolution (72–600) |
| Image format | `png`, `jpg`, `jpeg`, `webp` |
| Table strategy | `lines_strict`, `lines`, `text` |
| Margins | Page margins in points (0–200) |
| Page width | Page width in points (100–2000) |
| Write images to disk | Save extracted images to files |
| Embed images (base64) | Embed images as data URIs in markdown |
| Ignore images | Skip image extraction |
| Ignore graphics | Skip vector graphics |
| Page chunks | Split output by page |
| Force text | Force text extraction |
| Show progress | Show progress during conversion |
| Ignore code | Skip code blocks |
| **PDF engine** | **MarkItDown (default)** or **PyMuPDF4LLM (advanced)** |

> **PyMuPDF4LLM** requires optional dependency: `pip install pymupdf4llm` (or system package `python3-pymupdf`).

### PPTX
| Option | Description |
|---|---|
| Slides | Slide range: `1-5,7,10-N` |
| Disable presenter notes | Skip notes extraction |
| Add slide delimiters (`---`) | Insert `---` between slides |
| Disable image processing | Skip images entirely |
| Embed images as base64 | Include images as data URIs in markdown |
| **LLM image descriptions** | **Requires `OPENAI_API_KEY` env var** |
| LLM model | e.g. `gpt-4o`, `gpt-4-vision-preview` |
| Custom prompt | Custom prompt for image description |

> **Image handling**: MarkItDown PPTX converter does not save images to disk by default.
> - `Embed images as base64` → `![alt](data:image/...;base64,...)`
> - LLM model + API key → AI-generated descriptions of diagrams/charts
> - Neither → placeholder links like `![Figure 1](figure1.jpg)`

### Images (JPEG, PNG, WebP, BMP, TIFF)
| Option | Description |
|---|---|
| LLM model | Model for OCR/description (`gpt-4o`, etc.) |
| Custom prompt | Custom prompt for image analysis |

### Other formats (DOCX, XLSX, HTML, CSV, JSON, XML, EPUB, ZIP, Audio)
No format-specific options; uses MarkItDown defaults.

## Configuration

### LLM image descriptions
Set `OPENAI_API_KEY` environment variable:
```bash
export OPENAI_API_KEY="sk-..."
```

Or configure programmatically in code.

### ExifTool (for image metadata)
Install `exiftool` system package for EXIF extraction:
```bash
sudo apt install libimage-exiftool-perl  # Debian/Ubuntu
brew install exiftool                     # macOS
```

## Building from source

```bash
make build-deb    # .deb for Debian 13
make build-win    # .exe installer for Windows 10
make build-mac    # .dmg for macOS Tahoe 26
make build-all    # all three
```

## License

AGPL v3. Based on:
- [MarkItDown](https://github.com/microsoft/markitdown) — MIT (Microsoft)
- [PyMuPDF4LLM](https://github.com/pymupdf/pymupdf4llm) — AGPL v3 (Artifex)

## Links

- Repository: https://github.com/bettal/AnyFileToMarkdown
- Issues: https://github.com/bettal/AnyFileToMarkdown/issues