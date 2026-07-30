from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QSpinBox, QCheckBox, QGroupBox, QStackedWidget,
)


PAGE_PDF = 0
PAGE_PPTX = 1
PAGE_SIMPLE = 2


class OptionsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        self.stack.addWidget(self._build_pdf_page())
        self.stack.addWidget(self._build_pptx_page())
        self.stack.addWidget(self._build_simple_page())

        self.stack.setCurrentIndex(PAGE_SIMPLE)

    def _build_pdf_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        group = QGroupBox("PDF Options")
        grid = QVBoxLayout(group)

        r0 = QHBoxLayout()
        r0.addWidget(QLabel("Pages (e.g. 1-5,7,10-N):"))
        self.pdf_pages = QSpinBox()
        self.pdf_pages.setRange(1, 9999)
        r0.addWidget(self.pdf_pages)
        grid.addLayout(r0)

        r1 = QHBoxLayout()
        r1.addWidget(QLabel("DPI:"))
        self.pdf_dpi = QSpinBox()
        self.pdf_dpi.setRange(72, 600)
        self.pdf_dpi.setValue(150)
        r1.addWidget(self.pdf_dpi)
        r1.addSpacing(12)
        r1.addWidget(QLabel("Image format:"))
        self.pdf_img_fmt = QComboBox()
        self.pdf_img_fmt.addItems(["png", "jpg", "jpeg", "webp"])
        r1.addWidget(self.pdf_img_fmt)
        r1.addStretch()
        grid.addLayout(r1)

        r2 = QHBoxLayout()
        r2.addWidget(QLabel("Table strategy:"))
        self.pdf_table_strat = QComboBox()
        self.pdf_table_strat.addItems(["lines_strict", "lines", "text"])
        r2.addWidget(self.pdf_table_strat)
        r2.addSpacing(12)
        r2.addWidget(QLabel("Margins:"))
        self.pdf_margins = QSpinBox()
        self.pdf_margins.setRange(0, 200)
        self.pdf_margins.setValue(0)
        r2.addWidget(self.pdf_margins)
        r2.addSpacing(12)
        r2.addWidget(QLabel("Page width:"))
        self.pdf_pw = QSpinBox()
        self.pdf_pw.setRange(100, 2000)
        self.pdf_pw.setValue(612)
        r2.addWidget(self.pdf_pw)
        r2.addStretch()
        grid.addLayout(r2)

        flags = QHBoxLayout()
        self.pdf_write_img = QCheckBox("Write images to disk")
        self.pdf_embed_img = QCheckBox("Embed images (base64)")
        self.pdf_ignore_img = QCheckBox("Ignore images")
        self.pdf_ignore_gfx = QCheckBox("Ignore graphics")
        flags.addWidget(self.pdf_write_img)
        flags.addWidget(self.pdf_embed_img)
        flags.addWidget(self.pdf_ignore_img)
        flags.addWidget(self.pdf_ignore_gfx)
        grid.addLayout(flags)

        flags2 = QHBoxLayout()
        self.pdf_page_chunks = QCheckBox("Page chunks")
        self.pdf_force_text = QCheckBox("Force text")
        self.pdf_force_text.setChecked(True)
        self.pdf_show_progress = QCheckBox("Show progress")
        self.pdf_show_progress.setChecked(True)
        self.pdf_ignore_code = QCheckBox("Ignore code")
        flags2.addWidget(self.pdf_page_chunks)
        flags2.addWidget(self.pdf_force_text)
        flags2.addWidget(self.pdf_show_progress)
        flags2.addWidget(self.pdf_ignore_code)
        flags2.addStretch()
        grid.addLayout(flags2)

        engine_row = QHBoxLayout()
        engine_row.addWidget(QLabel("PDF engine:"))
        self.pdf_engine = QComboBox()
        self.pdf_engine.addItems(["MarkItDown (default)", "PyMuPDF4LLM (advanced)"])
        engine_row.addWidget(self.pdf_engine)
        engine_row.addStretch()
        grid.addLayout(engine_row)

        layout.addWidget(group)
        layout.addStretch()
        return page

    def _build_pptx_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        group = QGroupBox("PowerPoint Options")
        grid = QVBoxLayout(group)

        r0 = QHBoxLayout()
        r0.addWidget(QLabel("Slides (e.g. 1-5,7,10-N):"))
        self.pptx_slides = QSpinBox()
        self.pptx_slides.setRange(1, 9999)
        r0.addWidget(self.pptx_slides)
        grid.addLayout(r0)

        fl = QHBoxLayout()
        self.pptx_disable_notes = QCheckBox("Disable presenter notes")
        self.pptx_disable_image = QCheckBox("Disable image extraction")
        self.pptx_enable_slides = QCheckBox("Add slide delimiters (---)")
        fl.addWidget(self.pptx_disable_notes)
        fl.addWidget(self.pptx_disable_image)
        fl.addWidget(self.pptx_enable_slides)
        fl.addStretch()
        grid.addLayout(fl)

        layout.addWidget(group)
        layout.addStretch()
        return page

    def _build_simple_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        label = QLabel("No format-specific options available for this file type.")
        label.setStyleSheet("color: gray; padding: 20px;")
        layout.addWidget(label)
        layout.addStretch()
        return page

    def show_for_format(self, ext: str):
        if ext == ".pdf":
            self.stack.setCurrentIndex(PAGE_PDF)
        elif ext == ".pptx":
            self.stack.setCurrentIndex(PAGE_PPTX)
        else:
            self.stack.setCurrentIndex(PAGE_SIMPLE)
