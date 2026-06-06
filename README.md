# PythonChatGPT

Chatbot de terminal que se conecta a modelos locales vía [Ollama](https://ollama.ai/) usando la API compatible con OpenAI.

## Características

- Streaming de respuestas en tiempo real
- Persistencia de conversaciones (se guardan automáticamente)
- Exportación a Markdown
- Selector de modelos por flag CLI
- Retomar conversaciones anteriores
- Manejo de errores amigable

## Requisitos

- Python 3.10+
- [Ollama](https://ollama.ai/) instalado y corriendo

```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.2:1b
ollama serve
```

## Instalación

```bash
git clone https://github.com/alejandrojfs26-lgtm/PythonChatGPT.git
cd PythonChatGPT
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Uso

```bash
python main.py
python main.py --model llama3.1:8b
python main.py --resume
```

| Opción | Descripción |
|---|---|
| `--model, -m` | Modelo de Ollama a usar (default: `llama3.2:1b`) |
| `--resume, -r` | Retomar la última conversación guardada |

Comandos durante la conversación:

| Comando | Acción |
|---|---|
| `salir` | Termina y guarda la conversación |
| `exportar` | Exporta a Markdown sin salir |

## Tests

```bash
pip install pytest
pytest tests/
```

## Configuración

Variables de entorno (opcionales, se pueden sobreescribir con `--model`):

| Variable | Default | Descripción |
|---|---|---|
| `OLLAMA_URL` | `http://localhost:11434/v1` | URL de la API de Ollama |
| `OLLAMA_API_KEY` | `ollama` | API Key (Ollama no requiere autenticación) |
| `OLLAMA_MODEL` | `llama3.2:1b` | Modelo a usar |

## Licencia

MIT
