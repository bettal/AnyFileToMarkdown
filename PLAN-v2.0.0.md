# AnyFileToMarkdown v2.0.0 — План доработки

> Превращение ConvertPdfToMarkdown (PDF only) в AnyFileToMarkdown (универсальный конвертер)

---

## Стратегия

**Движок**: `microsoft/markitdown` (MIT, 170k ★) — основной
**PDF fallback**: `pymupdf4llm` — опционально, для тонких настроек PDF (DPI, table_strategy, margins)
**GUI**: PyQt6 — динамические опции в зависимости от выбранного формата

---

## 1. Переименование

| Сущность | Было | Стало |
|---|---|---|
| Пакет (pip) | `convert-pdf-to-markdown` | `anyfile-to-markdown` |
| Пакет (deb) | `convert-pdf-to-markdown` | `anyfile-to-markdown` |
| Директория | `pdf2md_gui/` | `anyfile_to_markdown/` |
| Бинарник | `/usr/bin/convert-pdf-to-markdown` | `/usr/bin/anyfile-to-markdown` |
| Desktop entry | `Convert PDF to Markdown` | `AnyFile to Markdown` |
| Иконки | `convert-pdf-to-markdown.*` | `anyfile-to-markdown.*` |
| Репозиторий | `bettal/ConvertPdfToMarkdown` | `bettal/AnyFileToMarkdown` |
| Версия | 1.0.6 | **2.0.0** |

## 2. Новая структура проекта

```
anyfile-to-markdown/
├── anyfile_to_markdown/
│   ├── __init__.py           # __version__ = "2.0.0"
│   ├── app.py                # AnyFileToMarkdownApp (главное окно)
│   ├── converters/
│   │   ├── __init__.py       # фабрика: выбор движка по формату
│   │   ├── markitdown_engine.py  # обёртка над markitdown
│   │   └── pymupdf_engine.py     # pymupdf4llm fallback (PDF)
│   ├── widgets/
│   │   ├── __init__.py
│   │   ├── format_selector.py    # автоопределение + QComboBox
│   │   └── options_panel.py      # динамические опции под формат
│   └── utils/
│       ├── __init__.py
│       └── page_parser.py        # _parse_pages (из app.py)
├── debian/                        # Debian 13 (trixie)
├── installer/
│   ├── anyfile-to-markdown.nsi   # NSIS для Windows 10
│   └── build-macos.sh            # .dmg для macOS Tahoe 26
├── icons/hicolor/
├── setup.py
├── Makefile
├── build-windows.spec             # PyInstaller Windows
└── PLAN-v2.0.0.md                 # этот файл
```

## 3. Архитектура GUI

```
┌──────────────────────────────────────┐
│  [AnyFile to Markdown]               │
├──────────────────────────────────────┤
│  File: [___________] [Browse...]     │
│  Format: [PDF ▼]  (автоопределение)  │
├──────────────────────────────────────┤
│  ┌─ Options ──────────────────────┐  │
│  │  PDF:    DPI, table_strategy,  │  │
│  │          margins, page_width,  │  │
│  │          image_format, flags   │  │
│  │  PPTX:   slides, notes,        │  │
│  │          disable_image         │  │
│  │  DOCX:   (без опций)           │  │
│  │  XLSX:   sheet_number          │  │
│  │  Image:  OCR language          │  │
│  │  HTML:   (без опций)           │  │
│  └────────────────────────────────┘  │
│                                       │
│  [Convert]                            │
├──────────────────────────────────────┤
│  Log: [...                    ]      │
└──────────────────────────────────────┘
```

## 4. Этапы работ (7 шагов)

### Этап 1: Переименование + структура
- [ ] `setup.py` — новый name, version=2.0.0, dependencies
- [ ] `anyfile_to_markdown/__init__.py` — __version__
- [ ] Создать `converters/`, `widgets/`, `utils/` с __init__.py
- [ ] Перенести `_parse_pages` в `utils/page_parser.py`
- [ ] Иконки: переименовать файлы

### Этап 2: markitdown engine
- [ ] `converters/markitdown_engine.py` — класс `MarkitdownEngine`
- [ ] Метод `convert(file_path, fmt, **kwargs)` → str
- [ ] Поддержка: PDF, PPTX, DOCX, XLSX, HTML, CSV, JSON, XML, EPUB, изображения
- [ ] Тест: конвертация каждого формата

### Этап 3: Новый GUI
- [ ] `widgets/format_selector.py` — автоопределение формата по расширению
- [ ] `widgets/options_panel.py` — QStackedWidget с панелями под каждый формат
- [ ] `app.py` — AnyFileToMarkdownApp: формат-селектор, динамические опции, convert
- [ ] Старые PDF-опции (DPI, table_strategy, margins, флаги) — в PDF-панель

### Этап 4: PDF fallback (pymupdf4llm)
- [ ] `converters/pymupdf_engine.py` — если `markitdown` не справляется с PDF
- [ ] Переключатель в GUI: "PDF engine: MarkItDown / PyMuPDF4LLM (advanced)"
- [ ] `setup.py` — `extras_require = {"pdf-advanced": ["pymupdf4llm"]}`

### Этап 5: Дебиан-пакет (Debian 13 Trixie)
- [ ] `debian/control` — обновить Source, Depends (markitdown вместо pymupdf4llm)
- [ ] `debian/rules` — PYBUILD_NAME, пути установки
- [ ] `debian/postinst` — проверка markitdown вместо pymupdf4llm
- [ ] `debian/install`, launcher, .desktop — новое имя
- [ ] `debian/bump-version.sh` — новый пакет

### Этап 6: Windows 10 (PyInstaller + NSIS)
- [ ] `build-windows.spec` — имя, hiddenimports для markitdown
- [ ] `installer/anyfile-to-markdown.nsi` — NSIS-скрипт:
  - Установка в `Program Files`
  - Иконка на рабочем столе
  - Запись в PATH
- [ ] Билд: `pyinstaller build-windows.spec` → `makensis installer/*.nsi`

### Этап 7: macOS Tahoe 26 (.app + .dmg)
- [ ] `build-macos.sh` — сборка:
  1. `pyinstaller --windowed --onefile --icon=icon.icns`
  2. `create-dmg` или `appdmg` → `.dmg`
- [ ] Иконка `anyfile-to-markdown.icns` (из SVG через iconutil)
- [ ] Info.plist для .app-бандла

## 5. Зависимости

```python
# setup.py
install_requires=[
    "PyQt6",
    "markitdown>=0.1.6",
    "markitdown[pptx,docx,xlsx,pdf]",
],
extras_require={
    "pdf-advanced": ["pymupdf4llm"],
    "ocr": ["markitdown[ocr]"],
    "all": ["markitdown[all]", "pymupdf4llm"],
}
```

**Debian 13 системные пакеты**:
- `python3-pyqt6`
- `python3-pip` (для markitdown из PyPI)
- `python3-pymupdf` (опционально, для PDF fallback)

## 6. Makefile цели

```makefile
build-deb:    # dpkg-buildpackage → .deb для Debian 13
build-win:    # PyInstaller + NSIS → .exe для Windows 10
build-mac:    # PyInstaller + create-dmg → .dmg для macOS Tahoe 26
build-all:    # всё сразу
release:      # bump-version + build-all
```

## 7. Оценка времени

| Этап | Часы |
|---|---|
| 1. Переименование + структура | 1 |
| 2. markitdown engine | 2 |
| 3. Новый GUI | 2-3 |
| 4. PDF fallback | 1 |
| 5. Debian 13 | 1 |
| 6. Windows 10 | 2-3 |
| 7. macOS Tahoe 26 | 2-3 |
| Тестирование кроссплатформа | 2 |
| **Итого** | **~11-15 ч** |
