# AnyFile to Markdown — Project Knowledge Base

## Description
Universal file to Markdown converter with PyQt6 GUI. Uses Microsoft MarkItDown engine.

## Package info
- **Package name:** `anyfile-to-markdown`
- **Binary:** `/usr/bin/anyfile-to-markdown`
- **Desktop entry:** `/usr/share/applications/anyfile-to-markdown.desktop`
- **Menu category:** Development (KDE Plasma / GNOME)

## Project structure
```
AnyFileToMarkdown/
├── anyfile_to_markdown/   # Python package
│   ├── app.py             # Main GUI window
│   ├── converters/        # Conversion engines
│   │   ├── markitdown_engine.py  # MarkItDown wrapper
│   │   └── pymupdf_engine.py     # PyMuPDF4LLM fallback (PDF)
│   ├── widgets/           # PyQt6 widgets
│   │   ├── format_selector.py    # Format auto-detection
│   │   └── options_panel.py      # Dynamic per-format options
│   └── utils/
│       └── page_parser.py        # Page range parser
├── debian/                # Debian packaging
├── installer/             # Windows (NSIS) + macOS (.dmg)
├── icons/                 # App icons
├── Makefile               # Build automation
├── setup.py               # Python package metadata
└── AGENTS.md              # This file
```

## Build commands
```bash
make build-deb    # .deb for Debian 13
make build-win    # .exe installer for Windows 10
make build-mac    # .dmg for macOS Tahoe 26
make build-all    # everything
make bump-patch   # increment version + update files
make release      # bump-patch + build-all
```

## Key dependencies (runtime)
- `markitdown[pptx,docx,xlsx,pdf]` (from PyPI, MIT)
- PyQt6 (system or pip)
- pymupdf4llm (optional, for advanced PDF options)

## Post-install logic (debian/postinst)
1. `apt-get install -f -y` — auto-fix dependencies
2. Install/upgrade `markitdown` via pip (--ignore-installed)
3. Quick import check
4. Update desktop/icon caches

## Version management
- `setup.py` and `debian/changelog` must stay in sync
- `debian/bump-version.sh` updates both
- Current version: 2.0.0

## Supported formats
PDF, PPTX, DOCX, XLSX, XLS, images (JPEG, PNG, WebP, BMP, TIFF),
HTML, CSV, JSON, XML, EPUB, ZIP, MP3, WAV

## GUI options per format

### PDF
- Pages, DPI, Image format, Table strategy, Margins, Page width
- Flags: write/embed/ignore images, ignore graphics, page chunks, force text, show progress, ignore code
- Engine: MarkItDown / PyMuPDF4LLM (advanced)

### PPTX
- Slides range, disable notes, slide delimiters, disable images, embed as base64
- LLM image descriptions (model, custom prompt) — requires OPENAI_API_KEY

### Images (JPEG, PNG, WebP, BMP, TIFF)
- LLM model + custom prompt for OCR/description

### Other formats
- No format-specific options (uses MarkItDown defaults)

## Image handling in PPTX (MarkItDown limitation)
MarkItDown PPTX converter **does not save images to disk**. Options:
1. **Embed as base64** — data URIs in markdown
2. **LLM description** — AI-generated text description (requires API key)
3. **Default** — placeholder links like `![Figure 1](figure1.jpg)`

## MarkItDown options (passed via kwargs)
- `llm_client`, `llm_model`, `llm_prompt` — LLM for image descriptions
- `exiftool_path` — EXIF metadata extraction
- `docintel_endpoint`, `docintel_credential`, `docintel_file_types`, `docintel_api_version` — Azure Document Intelligence