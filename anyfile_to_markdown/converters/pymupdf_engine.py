import os


SUPPORTED = {".pdf"}


class PymupdfEngine:
    def __init__(self):
        self._available = False
        self._module = None
        try:
            import pymupdf4llm
            self._module = pymupdf4llm
            self._available = True
        except ImportError:
            pass

    @property
    def available(self) -> bool:
        return self._available

    @staticmethod
    def supports(ext: str) -> bool:
        return ext.lower() in SUPPORTED

    def convert(self, path: str, **kwargs) -> str:
        from anyfile_to_markdown.utils.page_parser import parse_pages
        import pymupdf

        pages_arg = kwargs.pop("pages", None)
        if pages_arg is not None:
            with pymupdf.open(path) as doc:
                total = doc.page_count
            parsed = parse_pages(pages_arg, total)
            if parsed is not None:
                kwargs["pages"] = parsed

        return self._module.to_markdown(path, **kwargs)
