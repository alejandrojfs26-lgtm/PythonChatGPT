import json
import tempfile
from pathlib import Path

from config import Config


def test_config_defaults():
    c = Config()
    assert c.base_url == "http://localhost:11434/v1"
    assert c.api_key == "ollama"
    assert c.model == "llama3.2:1b"


def test_config_from_env(monkeypatch):
    monkeypatch.setenv("OLLAMA_URL", "http://localhost:8080/v1")
    monkeypatch.setenv("OLLAMA_MODEL", "llama3.1:8b")
    c = Config()
    assert c.base_url == "http://localhost:8080/v1"
    assert c.model == "llama3.1:8b"


def test_save_and_load_conversation():
    from main import _save_conversation, _load_last_conversation

    messages = [
        {"role": "system", "content": "Eres un asistente."},
        {"role": "user", "content": "Hola"},
        {"role": "assistant", "content": "¡Hola!"},
    ]

    with tempfile.TemporaryDirectory() as tmp:
        import main
        original_dir = main.CONVERSATIONS_DIR
        main.CONVERSATIONS_DIR = Path(tmp)

        path = _save_conversation(messages)
        assert path.exists()

        loaded = _load_last_conversation()
        assert loaded == messages

        main.CONVERSATIONS_DIR = original_dir


def test_export_markdown():
    from main import _export_markdown

    messages = [
        {"role": "user", "content": "¿Qué es Python?"},
        {"role": "assistant", "content": "Python es un lenguaje."},
    ]

    with tempfile.TemporaryDirectory() as tmp:
        import main
        original_dir = main.CONVERSATIONS_DIR
        main.CONVERSATIONS_DIR = Path(tmp)

        path = _export_markdown(messages)
        content = path.read_text()

        assert "## 👤 Tú" in content
        assert "¿Qué es Python?" in content
        assert "## 🤖 Asistente" in content
        assert "Python es un lenguaje." in content

        main.CONVERSATIONS_DIR = original_dir
