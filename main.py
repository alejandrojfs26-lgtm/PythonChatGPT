from openai import OpenAI
import typer
from rich import print
from rich.table import Table

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)


def main():
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

        response = client.chat.completions.create(
            model="llama3.2:1b",
            messages=messages,
        )

        response_assistant = response.choices[0].message.content
        messages.append({"role": "assistant", "content": response_assistant})
        print(response_assistant)


if __name__ == "__main__":
    typer.run(main)
