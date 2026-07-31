import sys
import os
import traceback
import threading
import datetime
import re
from urllib.parse import urlparse

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QFileDialog,
    QMessageBox, QMenuBar, QCheckBox,
)
from PyQt6.QtCore import Qt, pyqtSignal

from anyfile_to_markdown import __version__
from anyfile_to_markdown.widgets.format_selector import FormatSelector
from anyfile_to_markdown.widgets.options_panel import OptionsPanel
from anyfile_to_markdown.converters import engine_for


# ============================================================
# LLM Model URL Parser — парсит URL модели из браузера
# ============================================================

PROVIDER_CONFIG = {
    "openrouter.ai": {
        "name": "OpenRouter",
        "base_url": "https://openrouter.ai/api/v1",
        "model_pattern": r"openrouter\.ai/models/([^/?#]+)",
        "key_hint": "sk-or-...",
        "env_var": "OPENROUTER_API_KEY",
        "free_models": [
            "mistralai/pixtral-12b:free",
            "google/gemma-2-9b-it:free",
            "meta-llama/llama-3.2-11b-vision-instruct:free",
            "qwen/qwen2.5-vl-7b-instruct:free",
        ],
    },
    "groq.com": {
        "name": "Groq",
        "base_url": "https://api.groq.com/openai/v1",
        "model_pattern": r"groq\.com/models/([^/?#]+)",
        "key_hint": "gsk_...",
        "env_var": "GROQ_API_KEY",
        "free_models": [
            "llama-3.2-90b-vision-preview",
            "llama-3.2-11b-vision-preview",
        ],
    },
    "github.com": {
        "name": "GitHub Models",
        "base_url": "https://models.inference.ai.azure.com",
        "model_pattern": r"github\.com/marketplace/models/([^/?#]+)",
        "key_hint": "github_pat_...",
        "env_var": "GITHUB_TOKEN",
        "free_models": [
            "gpt-4o",
            "Phi-3.5-vision",
            "Llama-3.2-90B-Vision",
            "Llama-3.2-11B-Vision",
        ],
    },
    "together.ai": {
        "name": "Together AI",
        "base_url": "https://api.together.xyz/v1",
        "model_pattern": r"together\.ai/models/([^/?#]+)",
        "key_hint": "together_...",
        "env_var": "TOGETHER_API_KEY",
        "free_models": [
            "meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo",
            "meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo",
        ],
    },
    "nvidia.com": {
        "name": "NVIDIA NIM",
        "base_url": "https://integrate.api.nvidia.com/v1",
        "model_pattern": r"nvidia\.com/([^/?#]+)",
        "key_hint": "nvapi_...",
        "env_var": "NVIDIA_API_KEY",
        "free_models": [
            "nvidia/llama-3.2-90b-vision",
        ],
    },
}


def parse_model_url(url: str) -> dict | None:
    """
    Парсит URL модели и возвращает конфиг провайдера + model_id.
    Поддерживаемые форматы:
      - https://openrouter.ai/models/mistralai/pixtral-12b:free
      - https://console.groq.com/models/llama-3.2-90b-vision-preview
      - https://github.com/marketplace/models/azureml-gpt4o
      - https://together.ai/models/meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo
      - https://build.nvidia.com/explore/discover/nvidia/llama-3.2-90b-vision
    """
    if not url or not url.strip():
        return None
    
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    
    try:
        parsed = urlparse(url)
        hostname = parsed.netloc.lower().replace("www.", "").replace("console.", "").replace("api.", "")
        
        # Находим провайдера
        provider_key = None
        for key in PROVIDER_CONFIG:
            if key in hostname:
                provider_key = key
                break
        
        if not provider_key:
            return None
        
        config = PROVIDER_CONFIG[provider_key]
        
        # Извлекаем model_id из path
        path = parsed.path
        pattern = config["model_pattern"]
        match = re.search(pattern, path)
        
        if match:
            model_id = match.group(1)
        else:
            # Fallback: последняя часть path
            parts = [p for p in path.split("/") if p]
            model_id = parts[-1] if parts else ""
        
        # Очистка model_id
        model_id = model_id.rstrip("/")
        
        return {
            "provider": config["name"],
            "provider_key": provider_key,
            "base_url": config["base_url"],
            "model_id": model_id,
            "key_hint": config["key_hint"],
            "env_var": config["env_var"],
            "free_models": config["free_models"],
        }
    except Exception:
        return None


def build_llm_kwargs(parsed: dict, api_key: str = "") -> dict:
    """
    Строит kwargs для MarkItDown из распарсенного URL и API ключа.
    """
    if not parsed:
        return {}
    
    kwargs = {
        "llm_model": parsed["model_id"],
    }
    
    # API ключ: приоритет — введённый пользователем, потом env var
    if api_key and api_key.strip():
        from openai import OpenAI
        kwargs["llm_client"] = OpenAI(
            base_url=parsed["base_url"],
            api_key=api_key.strip(),
        )
    else:
        # Попробуем взять из env
        import os
        env_key = os.getenv(parsed["env_var"])
        if env_key:
            from openai import OpenAI
            kwargs["llm_client"] = OpenAI(
                base_url=parsed["base_url"],
                api_key=env_key,
            )
    
    return kwargs


# ============================================================
# Test
# ============================================================
if __name__ == "__main__":
    test_urls = [
        "https://openrouter.ai/models/mistralai/pixtral-12b:free",
        "https://console.groq.com/models/llama-3.2-90b-vision-preview",
        "https://github.com/marketplace/models/azureml-gpt4o",
        "https://together.ai/models/meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo",
        "https://build.nvidia.com/explore/discover/nvidia/llama-3.2-90b-vision",
    ]
    
    for url in test_urls:
        result = parse_model_url(url)
        print(f"\nURL: {url}")
        if result:
            print(f"  Provider: {result['provider']}")
            print(f"  Base URL: {result['base_url']}")
            print(f"  Model ID: {result['model_id']}")
            print(f"  Key hint: {result['key_hint']}")
            print(f"  Free models: {result['free_models']}")
        else:
            print("  FAILED TO PARSE")