# PythonChatGPT

Chatbot de terminal que se conecta a modelos locales vía [Ollama](https://ollama.ai/) usando la API compatible con OpenAI.

## Requisitos

- Python 3.10+
- [Ollama](https://ollama.ai/) instalado y corriendo con al menos un modelo descargado

```bash
# Instalar Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Descargar un modelo
ollama pull llama3.2:1b

# Iniciar Ollama
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
```

Escribe tu pregunta y presiona Enter. Escribe `salir` para terminar.

## Configuración

Variables de entorno (opcionales):

| Variable | Default | Descripción |
|---|---|---|
| `OLLAMA_URL` | `http://localhost:11434/v1` | URL de la API de Ollama |
| `OLLAMA_API_KEY` | `ollama` | API Key (Ollama no requiere autenticación) |
| `OLLAMA_MODEL` | `llama3.2:1b` | Modelo a usar |

## Licencia

MIT
