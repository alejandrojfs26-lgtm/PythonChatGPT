from openai import OpenAI
from openai import APIConnectionError
import typer
from rich import print
from rich.table import Table
import os

BASE_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/v1")
API_KEY = os.getenv("OLLAMA_API_KEY", "ollama")
MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)


def main() -> None:
    print("[bold yellow]Chat-bot con IA (Ollama)[/bold yellow]")

    table = Table("Opciones", "Descripción")
    table.add_row("Salir", "Escribir 'salir' para salir del programa")
    print(table)

    messages = [
        {"role": "system", "content": "Eres un asistente muy util."}
    ]

    while True:
        content = input("Escribe tu pregunta: ")
        if content == "salir":
            break
        messages.append({"role": "user", "content": content})

        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                stream=True,
            )

            assistant_reply = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    content_chunk = chunk.choices[0].delta.content
                    print(content_chunk, end="")
                    assistant_reply += content_chunk
            print()

            messages.append({"role": "assistant", "content": assistant_reply})
        except APIConnectionError:
            print("\n[red]Error: No se pudo conectar a Ollama.[/red]")
            print("[yellow]Asegúrate de que Ollama esté corriendo:[/yellow]")
            print("  ollama serve")
            break


if __name__ == "__main__":
    typer.run(main)
