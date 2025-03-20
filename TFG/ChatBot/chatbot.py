from openai import OpenAI
from ChatBot import config
import typer
from rich import print
from rich.table import Table

def main():
    client = OpenAI(
        base_url=config.base_url,
        api_key=config.api_key
    )
    
    print("[bold green]🔐 ChatGPT API en Python[/bold green]")

    table = Table("Comando", "Descripción")
    table.add_row("new", "Nueva conversación") 
    table.add_row("exit", "Volver al menú")
    
    print(table)

    mensajes=[{"role": "system", "content": "Eres un asistente muy útil."}]
    contexto = [mensajes]
    
    while True:
        content = __prompt()

        if content == "exit":
            print("🤸‍♂️ Volviendo al menú...")
            return "exit"

        if content == "new":
            print("🆕 Nueva conversación creada")
            mensajes = [contexto]
            content = __prompt()

        mensajes.append({"role": "user", "content": content})

        respuesta = client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=mensajes
        )
        
        respuesta_content = respuesta.choices[0].message.content
        
        mensajes.append({"role": "assistant", "content": respuesta_content})

        print(f"[bold green]> [/bold green][green]{respuesta_content}[/green]")

def __prompt() -> str:
    prompt = typer.prompt("\n¿Sobre qué quieres hablar?")

    if prompt == "exit":
        return "exit"
    
    return prompt

if __name__ == "__main__":
    typer.run(main)
