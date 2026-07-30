import sys
import os
import traceback
import threading
import datetime
from importlib.metadata import version

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QComboBox, QCheckBox,
    QSpinBox, QTextEdit, QFileDialog, QMessageBox, QGroupBox,
    QMenuBar
)
from PyQt6.QtCore import Qt, pyqtSignal

from markitdown import MarkItDown

from anyfile_to_markdown import __version__

SUPPORTED_FORMATS = {
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


class AnyFileToMarkdownApp(QMainWindow):
    log_signal = pyqtSignal(str)
    conversion_done = pyqtSignal(str, str, str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("AnyFile to Markdown")
        self.resize(720, 720)

        self.input_path = ""
        self.output_path = ""
        self.log_file = None

        self.log_signal.connect(self._append_log)
        self.conversion_done.connect(self._on_conversion_done)

        self._create_menu()

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(12, 12, 12, 12)

        input_group = QGroupBox("Input File")
        input_row = QHBoxLayout(input_group)
        self.open_btn = QPushButton("Browse...")
        self.open_btn.clicked.connect(self._browse_file)
        self.file_label = QLabel()
        self.file_label.setStyleSheet("color: gray")
        input_row.addWidget(self.open_btn)
        input_row.addWidget(self.file_label, 1)
        layout.addWidget(input_group)

        self.fmt_label = QLabel()
        layout.addWidget(self.fmt_label)

        out_group = QGroupBox("Output")
        out_row = QHBoxLayout(out_group)
        self.out_btn = QPushButton("Save as...")
        self.out_btn.clicked.connect(self._browse_output)
        self.out_label = QLabel()
        self.out_label.setStyleSheet("color: gray")
        out_row.addWidget(self.out_btn)
        out_row.addWidget(self.out_label, 1)
        layout.addWidget(out_group)

        opts_group = QGroupBox("Options")
        opts_grid = QVBoxLayout(opts_group)

        r0 = QHBoxLayout()
        r0.addWidget(QLabel("Pages (e.g. 1-5,7,10-N):"))
        self.pages_edit = QLineEdit()
        r0.addWidget(self.pages_edit)
        opts_grid.addLayout(r0)

        r1 = QHBoxLayout()
        r1.addWidget(QLabel("DPI:"))
        self.dpi_spin = QSpinBox()
        self.dpi_spin.setRange(72, 600)
        self.dpi_spin.setValue(150)
        r1.addWidget(self.dpi_spin)
        r1.addSpacing(12)
        r1.addWidget(QLabel("Image format:"))
        self.img_fmt = QComboBox()
        self.img_fmt.addItems(["png", "jpg", "jpeg", "webp"])
        r1.addWidget(self.img_fmt)
        r1.addStretch()
        opts_grid.addLayout(r1)

        r2 = QHBoxLayout()
        r2.addWidget(QLabel("Table strategy:"))
        self.table_strat = QComboBox()
        self.table_strat.addItems(["lines_strict", "lines", "text"])
        r2.addWidget(self.table_strat)
        r2.addSpacing(12)
        r2.addWidget(QLabel("Margins:"))
        self.margins_spin = QSpinBox()
        self.margins_spin.setRange(0, 200)
        self.margins_spin.setValue(0)
        r2.addWidget(self.margins_spin)
        r2.addSpacing(12)
        r2.addWidget(QLabel("Page width:"))
        self.pw_spin = QSpinBox()
        self.pw_spin.setRange(100, 2000)
        self.pw_spin.setValue(612)
        r2.addWidget(self.pw_spin)
        r2.addStretch()
        opts_grid.addLayout(r2)

        layout.addWidget(opts_group)

        flags_group = QGroupBox("Flags")
        flags_row = QHBoxLayout(flags_group)
        self.cb_write_img = QCheckBox("Write images to disk")
        self.cb_embed_img = QCheckBox("Embed images (base64)")
        self.cb_ignore_img = QCheckBox("Ignore images")
        self.cb_ignore_gfx = QCheckBox("Ignore graphics")
        flags_row.addWidget(self.cb_write_img)
        flags_row.addWidget(self.cb_embed_img)
        flags_row.addWidget(self.cb_ignore_img)
        flags_row.addWidget(self.cb_ignore_gfx)
        layout.addWidget(flags_group)

        flags2_group = QGroupBox()
        flags2_row = QHBoxLayout(flags2_group)
        flags2_row.setContentsMargins(0, 0, 0, 0)
        self.cb_page_chunks = QCheckBox("Page chunks")
        self.cb_force_text = QCheckBox("Force text")
        self.cb_force_text.setChecked(True)
        self.cb_show_progress = QCheckBox("Show progress")
        self.cb_show_progress.setChecked(True)
        self.cb_ignore_code = QCheckBox("Ignore code")
        flags2_row.addWidget(self.cb_page_chunks)
        flags2_row.addWidget(self.cb_force_text)
        flags2_row.addWidget(self.cb_show_progress)
        flags2_row.addWidget(self.cb_ignore_code)
        flags2_row.addStretch()
        layout.addWidget(flags2_group)

        self.convert_btn = QPushButton("Convert")
        self.convert_btn.clicked.connect(self._convert)
        layout.addWidget(self.convert_btn)

        log_group = QGroupBox("Log")
        log_layout = QVBoxLayout(log_group)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        layout.addWidget(log_group, 1)

    def _create_menu(self):
        menubar = self.menuBar()
        help_menu = menubar.addMenu("Help")
        help_menu.addAction("About", self._show_about)

    def _show_about(self):
        QMessageBox.about(
            self,
            "About AnyFile to Markdown",
            f"<b>AnyFile to Markdown</b><br>"
            f"Version: {__version__}<br>"
            f"Author: stas<br>"
            f"License: GNU AGPL v3<br><br>"
            f"Engine: MarkItDown by Microsoft<br>"
            f"<a href='https://github.com/bettal/AnyFileToMarkdown'>Repository</a>"
        )

    def _detect_format(self, path):
        ext = os.path.splitext(path)[1].lower()
        return SUPPORTED_FORMATS.get(ext, "Unknown format")

    def _browse_file(self):
        filters = (
            "Supported files (*.pdf *.pptx *.docx *.xlsx *.xls "
            "*.jpg *.jpeg *.png *.webp *.bmp *.tiff *.tif "
            "*.html *.htm *.csv *.json *.xml *.epub *.zip "
            "*.mp3 *.wav);;"
            "All files (*.*)"
        )
        path, _ = QFileDialog.getOpenFileName(self, "Select file", "", filters)
        if path:
            self.input_path = path
            self.file_label.setText(path)
            fmt = self._detect_format(path)
            self.fmt_label.setText(f"Detected format: {fmt}")
            default_out = os.path.splitext(path)[0] + ".md"
            if not self.output_path:
                self.output_path = default_out
                self.out_label.setText(default_out)

    def _browse_output(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save markdown as", "", "Markdown files (*.md);;All files (*.*)"
        )
        if path:
            self.output_path = path
            self.out_label.setText(path)

    def _log(self, msg):
        self.log_signal.emit(msg)

    def _append_log(self, msg):
        stamp = datetime.datetime.now().strftime("%H:%M:%S")
        line = f"[{stamp}] {msg}"
        self.log_text.append(line)
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )
        if self.log_file:
            self.log_file.write(line + "\n")
            self.log_file.flush()

    def _on_conversion_done(self, status, title, message):
        self.convert_btn.setEnabled(True)
        self.convert_btn.setText("Convert")
        if self.log_file:
            self.log_file.close()
            self.log_file = None
        if status == "success":
            QMessageBox.information(self, title, message)
        else:
            QMessageBox.critical(self, title, message)

    def _convert(self):
        if not self.input_path or not os.path.isfile(self.input_path):
            QMessageBox.critical(self, "Error", "Please select a valid file.")
            return

        out = self.output_path or os.path.splitext(self.input_path)[0] + ".md"
        self.output_path = out
        self.out_label.setText(out)

        self.convert_btn.setEnabled(False)
        self.convert_btn.setText("Converting...")
        self.log_text.clear()

        log_path = out + ".log"
        try:
            if self.log_file:
                self.log_file.close()
            self.log_file = open(log_path, "w", encoding="utf-8")
        except Exception:
            self.log_file = None

        thread = threading.Thread(
            target=self._run_conversion, args=(self.input_path, out), daemon=True
        )
        thread.start()

    def _run_conversion(self, path, out):
        try:
            self._log(f"Opening: {path}")
            fmt = self._detect_format(path)
            self._log(f"Format: {fmt}")
            self._log(f"Output: {out}")

            self._log("Converting with MarkItDown...")
            md = MarkItDown()
            result = md.convert(path)
            md_text = result.markdown

            if not md_text:
                self._log("WARNING: Conversion returned empty result!")

            with open(out, "w", encoding="utf-8") as f:
                f.write(md_text)

            self._log(f"Done! Saved to: {out}")
            self._log(
                f"Output size: {len(md_text)} chars / "
                f"~{len(md_text.splitlines())} lines"
            )

            self.conversion_done.emit(
                "success", "Success",
                f"Converted successfully!\nSaved to:\n{out}"
            )

        except Exception as e:
            self._log(f"ERROR: {e}")
            self._log(f"TRACEBACK:\n{traceback.format_exc()}")
            self.conversion_done.emit("error", "Error", str(e))


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("AnyFile to Markdown")
    app.setDesktopFileName("anyfile-to-markdown")
    window = AnyFileToMarkdownApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
