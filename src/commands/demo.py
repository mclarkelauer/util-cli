"""Demo command using standard click registration."""
import asyncio
import asyncclick as click
from rich.console import Console

console = Console()

@click.command()
@click.option("--name", default="World", help="Name to greet")
@click.option("--count", default=1, help="Number of greetings")
async def demo(name, count):
    """Demo async command to showcase async/await functionality."""
    console.print(f"[bold green]Running demo command with async/await![/bold green]")
    
    for i in range(count):
        console.print(f"[blue]Hello, {name}! (greeting {i+1})[/blue]")
        await asyncio.sleep(0.5)  # Simulate async work
    
    console.print("[bold yellow]Demo completed![/bold yellow]")