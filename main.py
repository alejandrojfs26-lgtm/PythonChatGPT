from openai import OpenAI
from openai import APIConnectionError
import typer
from rich import print
from rich.table import Table
from datetime import datetime
import json
from pathlib import Path

from config import config

CONVERSATIONS_DIR = Path("conversations")


def _load_last_conversation() -> list[dict]:
    if not CONVERSATIONS_DIR.exists():
        return []
    files = sorted(CONVERSATIONS_DIR.glob("*.json"), reverse=True)
    if not files:
        return []
    return json.loads(files[0].read_text())


def _save_conversation(messages: list[dict]) -> Path:
    CONVERSATIONS_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = CONVERSATIONS_DIR / f"chat_{timestamp}.json"
    path.write_text(json.dumps(messages, indent=2, ensure_ascii=False))
    return path


def _export_markdown(messages: list[dict]) -> Path:
    lines = ["# Conversación - PythonChatGPT\n"]
    for msg in messages:
        role = {"system": "🔧 Sistema", "user": "👤 Tú", "assistant": "🤖 Asistente"}.get(msg["role"], msg["role"])
        lines.append(f"## {role}\n")
        lines.append(f"{msg['content']}\n")
    path = CONVERSATIONS_DIR / f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    path.write_text("\n".join(lines))
    return path


def main(
    model: str = typer.Option(config.model, "--model", "-m", help="Modelo de Ollama a usar"),
    resume: bool = typer.Option(False, "--resume", "-r", help="Retomar la última conversación"),
) -> None:
    client = OpenAI(base_url=config.base_url, api_key=config.api_key)

    print("[bold yellow]Chat-bot con IA (Ollama)[/bold yellow]")
    print(f"  Modelo: [cyan]{model}[/cyan]")
    print(f"  Servidor: [cyan]{config.base_url}[/cyan]")

    table = Table("Opciones", "Descripción")
    table.add_row("salir", "Terminar la conversación")
    table.add_row("exportar", "Exportar la conversación a Markdown")
    print(table)

    if resume:
        messages = _load_last_conversation()
        if messages:
            print("[green]Conversación retomada.[/green]")
        else:
            print("[yellow]No hay conversaciones previas. Empezando nueva.[/yellow]")
            messages = [{"role": "system", "content": "Eres un asistente muy util."}]
    else:
        messages = [{"role": "system", "content": "Eres un asistente muy util."}]

    while True:
        content = input("\n[bold cyan]Escribe tu pregunta: [/bold cyan]")
        if content == "salir":
            break
        if content == "exportar":
            md_path = _export_markdown(messages)
            print(f"[green]Conversación exportada a: {md_path}[/green]")
            continue

        messages.append({"role": "user", "content": content})

        try:
            response = client.chat.completions.create(
                model=model,
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

    _save_conversation(messages)
    md_path = _export_markdown(messages)
    print(f"\n[green]Conversación guardada. Exportada a: {md_path}[/green]")


if __name__ == "__main__":
    typer.run(main)
