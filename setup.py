from setuptools import setup, find_packages

setup(
    name="anyfile-to-markdown",
    version="2.0.0",
    description="Universal file to Markdown converter — PDF, DOCX, PPTX, XLSX, images, HTML, EPUB and more",
    long_description=open("README.md").read() if __import__("os").path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    author="stas",
    url="https://github.com/bettal/AnyFileToMarkdown",
    license="GNU AGPL v3",
    license_files=["LICENSE"],
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "PyQt6",
        "markitdown>=0.1.6",
    ],
    extras_require={
        "pdf-advanced": ["pymupdf4llm"],
        "ocr": ["markitdown[ocr]"],
        "all": ["markitdown[all]", "pymupdf4llm"],
    },
    entry_points={
        "console_scripts": [
            "anyfile-to-markdown=anyfile_to_markdown.app:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Natural Language :: Russian",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
    ],
)
