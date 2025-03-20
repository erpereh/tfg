from ChatBot import chatbot
import typer
from rich import print
from rich.table import Table

app = typer.Typer()

def main():
    while True:
        table = Table("Comando", "Descripción")
        table.add_row("1", "ChatBot")
        table.add_row("2", "Nueva")
        table.add_row("exit", "Salir de la aplicación")
        
        print(table)
        
        option = __prompt()
        if option == "exit":
            print("👋 ¡Hasta luego!")
            break
            

def __prompt() -> str:
    prompt = typer.prompt("\nEscoge una opción: ")
    
    if prompt == "1":
        result = chatbot.main() 
        if result == "exit":
            return
    elif prompt == "exit":
        return "exit"

    return prompt
    
if __name__ == "__main__":
    typer.run(main)
