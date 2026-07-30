import os

from markitdown import MarkItDown


SUPPORTED = {
    ".pdf", ".pptx", ".docx", ".xlsx", ".xls",
    ".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif",
    ".html", ".htm", ".csv", ".json", ".xml",
    ".epub", ".zip",
    ".mp3", ".wav",
}


class MarkitdownEngine:
    def __init__(self, llm_client=None, llm_model=None):
        kwargs = {}
        if llm_client and llm_model:
            kwargs["llm_client"] = llm_client
            kwargs["llm_model"] = llm_model
        self._md = MarkItDown(**kwargs)

    @staticmethod
    def supports(ext: str) -> bool:
        return ext.lower() in SUPPORTED

    def convert(self, path: str, **kwargs) -> str:
        result = self._md.convert(path)
        return result.markdown
