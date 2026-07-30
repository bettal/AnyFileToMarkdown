import os

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox
from PyQt6.QtCore import pyqtSignal


FORMAT_MAP = {
    ".pdf":  "PDF Document",
    ".pptx": "PowerPoint Presentation",
    ".docx": "Word Document",
    ".xlsx": "Excel Spreadsheet",
    ".xls":  "Excel Spreadsheet (old)",
    ".jpg":  "JPEG Image",
    ".jpeg": "JPEG Image",
    ".png":  "PNG Image",
    ".webp":"WebP Image",
    ".bmp":  "BMP Image",
    ".tiff": "TIFF Image",
    ".tif":  "TIFF Image",
    ".html": "HTML Document",
    ".htm":  "HTML Document",
    ".csv":  "CSV Data",
    ".json": "JSON Data",
    ".xml":  "XML Data",
    ".epub": "EPUB E-book",
    ".zip":  "ZIP Archive",
    ".mp3":  "MP3 Audio",
    ".wav":  "WAV Audio",
}


def detect_format(path: str):
    ext = os.path.splitext(path)[1].lower()
    return FORMAT_MAP.get(ext, "Unknown format"), ext


class FormatSelector(QWidget):
    format_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel("Format:")
        layout.addWidget(self.label)

        self.combo = QComboBox()
        self.combo.addItem("Auto-detect")
        for name in sorted(set(FORMAT_MAP.values())):
            self.combo.addItem(name)
        self.combo.setCurrentIndex(0)
        self.combo.currentTextChanged.connect(self._on_change)
        layout.addWidget(self.combo, 1)

        self._current_ext = ""

    def _on_change(self, text):
        self.format_changed.emit(text)

    def set_from_path(self, path: str):
        name, ext = detect_format(path)
        self._current_ext = ext
        idx = self.combo.findText(name)
        if idx >= 0:
            self.combo.setCurrentIndex(idx)
        else:
            self.combo.setCurrentIndex(0)

    @property
    def current_ext(self) -> str:
        return self._current_ext
