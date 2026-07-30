from anyfile_to_markdown.converters.markitdown_engine import MarkitdownEngine
from anyfile_to_markdown.converters.pymupdf_engine import PymupdfEngine


def engine_for(ext: str):
    if PymupdfEngine.supports(ext) and PymupdfEngine().available:
        return PymupdfEngine()
    if MarkitdownEngine.supports(ext):
        return MarkitdownEngine()
    return None
