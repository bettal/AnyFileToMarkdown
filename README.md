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

## Installation

### Debian 13 (Trixie)

```bash
sudo dpkg -i dist/anyfile-to-markdown_*.deb
sudo apt-get install -f
```

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

## Build from source

```bash
make build-deb   # Debian .deb
make build-win   # Windows .exe (requires PyInstaller + NSIS)
make build-mac   # macOS .dmg (requires PyInstaller + create-dmg)
make build-all   # all three
```

## License

AGPL v3. Based on [MarkItDown](https://github.com/microsoft/markitdown) by Microsoft (MIT) and [PyMuPDF4LLM](https://github.com/pymupdf/pymupdf4llm) by Artifex (AGPL v3).
