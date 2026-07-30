import sys
import os
import traceback
import threading
import datetime

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSpinBox, QTextEdit, QFileDialog,
    QMessageBox, QMenuBar,
)
from PyQt6.QtCore import Qt, pyqtSignal

from anyfile_to_markdown import __version__
from anyfile_to_markdown.widgets.format_selector import FormatSelector
from anyfile_to_markdown.widgets.options_panel import OptionsPanel
from anyfile_to_markdown.converters import engine_for


SUPPORTED_EXTS = {
    ".pdf", ".pptx", ".docx", ".xlsx", ".xls",
    ".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif",
    ".html", ".htm", ".csv", ".json", ".xml",
    ".epub", ".zip",
    ".mp3", ".wav",
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

        file_row = QHBoxLayout()
        self.open_btn = QPushButton("Browse...")
        self.open_btn.clicked.connect(self._browse_file)
        self.file_label = QLabel()
        self.file_label.setStyleSheet("color: gray")
        file_row.addWidget(self.open_btn)
        file_row.addWidget(self.file_label, 1)
        layout.addLayout(file_row)

        self.fmt_selector = FormatSelector()
        layout.addWidget(self.fmt_selector)

        out_row = QHBoxLayout()
        self.out_btn = QPushButton("Save as...")
        self.out_btn.clicked.connect(self._browse_output)
        self.out_label = QLabel()
        self.out_label.setStyleSheet("color: gray")
        out_row.addWidget(self.out_btn)
        out_row.addWidget(self.out_label, 1)
        layout.addLayout(out_row)

        self.options_panel = OptionsPanel()
        layout.addWidget(self.options_panel)

        self.convert_btn = QPushButton("Convert")
        self.convert_btn.clicked.connect(self._convert)
        layout.addWidget(self.convert_btn)

        log_group = QTextEdit()
        log_group.setReadOnly(True)
        self.log_text = log_group
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

    def _browse_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select file", "")
        if path:
            self.input_path = path
            self.file_label.setText(path)
            self.fmt_selector.set_from_path(path)
            ext = self.fmt_selector.current_ext
            self.options_panel.show_for_format(ext)
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

        ext = self.fmt_selector.current_ext
        thread = threading.Thread(
            target=self._run_conversion,
            args=(self.input_path, out, ext),
            daemon=True,
        )
        thread.start()

    def _run_conversion(self, path, out, ext):
        try:
            self._log(f"Opening: {path}")
            self._log(f"Format: {ext}")
            self._log(f"Output: {out}")

            engine = engine_for(ext)
            if engine is None:
                raise ValueError(f"No converter available for format: {ext}")

            self._log(f"Using: {type(engine).__name__}")

            kwargs = {}
            if ext == ".pdf":
                pages_raw = str(self.options_panel.pdf_pages.value())
                if pages_raw.strip():
                    kwargs["pages"] = pages_raw
                use_pymupdf = self.options_panel.pdf_engine.currentIndex() == 1
                if use_pymupdf and ext == ".pdf":
                    from anyfile_to_markdown.converters.pymupdf_engine import PymupdfEngine
                    pdf_engine = PymupdfEngine()
                    if pdf_engine.available:
                        engine = pdf_engine
                        kwargs["dpi"] = self.options_panel.pdf_dpi.value()
                        kwargs["image_format"] = self.options_panel.pdf_img_fmt.currentText()
                        kwargs["table_strategy"] = self.options_panel.pdf_table_strat.currentText()
                        kwargs["page_width"] = self.options_panel.pdf_pw.value()
                        kwargs["margins"] = self.options_panel.pdf_margins.value()
                        kwargs["write_images"] = self.options_panel.pdf_write_img.isChecked()
                        kwargs["embed_images"] = self.options_panel.pdf_embed_img.isChecked()
                        kwargs["ignore_images"] = self.options_panel.pdf_ignore_img.isChecked()
                        kwargs["ignore_graphics"] = self.options_panel.pdf_ignore_gfx.isChecked()
                        kwargs["page_chunks"] = self.options_panel.pdf_page_chunks.isChecked()
                        kwargs["force_text"] = self.options_panel.pdf_force_text.isChecked()
                        kwargs["show_progress"] = self.options_panel.pdf_show_progress.isChecked()
                        kwargs["ignore_code"] = self.options_panel.pdf_ignore_code.isChecked()

            self._log("Converting to Markdown...")
            md_text = engine.convert(path, **kwargs)

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
