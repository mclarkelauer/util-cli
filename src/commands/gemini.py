"""Gemini AI chat commands."""
import asyncio
import asyncclick as click
from util.logging import logger

def _get_console():
    """Lazy import Console to improve startup time."""
    from rich.console import Console
    return Console()

def _get_genai():
    """Lazy import genai to improve startup time."""
    from google import genai
    return genai

def _get_markdown():
    """Lazy import Markdown to improve startup time.""" 
    from rich.markdown import Markdown
    return Markdown

class AsyncGemini:
    """Async wrapper for Gemini AI client."""
    
    Client = None

    def __init__(self, apikey, version="gemini-2.0-flash"):
        self.apikey = apikey
        self.version = version
        genai = _get_genai()
        self.client = genai.Client(api_key=self.apikey)

    async def request(self, text):
        """Send a single request to Gemini."""
        try:
            # Run the blocking operation in a thread pool
            response = await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: self.client.models.generate_content(
                    model=self.version, 
                    contents=[text]
                )
            )
            return response.text
        except Exception as e:
            logger.error(f"Error making Gemini request: {e}")
            raise

    async def chat(self):
        """Start an interactive chat session with Gemini."""
        try:
            # Create chat session
            chat = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.chats.create(model=self.version)
            )
            
            console = _get_console()
            console.print("[bold green]🤖 Gemini Chat Session Started[/bold green]")
            console.print("[dim]Type 'quit' or 'q' to exit[/dim]")
            console.print("-" * 50)

            while True:
                try:
                    # Get user input
                    prompt_text = await asyncio.get_event_loop().run_in_executor(
                        None,
                        lambda: click.prompt("You", type=str)
                    )
                    
                    if prompt_text.lower() in ["q", "quit", "exit"]:
                        console.print("[yellow]Goodbye! 👋[/yellow]")
                        break
                    
                    # Send message to Gemini asynchronously
                    console.print("[dim]Thinking...[/dim]")
                    response = await asyncio.get_event_loop().run_in_executor(
                        None,
                        lambda: chat.send_message(prompt_text)
                    )
                    
                    # Display response with rich markdown formatting
                    console.print("[bold blue]Gemini:[/bold blue]")
                    Markdown = _get_markdown()
                    md = Markdown(response.text)
                    console.print(md)
                    console.print("-" * 50)
                    
                except KeyboardInterrupt:
                    console.print("\\n[yellow]Chat interrupted. Goodbye! 👋[/yellow]")
                    break
                except Exception as e:
                    console.print(f"[red]Error in chat: {e}[/red]")
                    continue
                    
        except Exception as e:
            console.print(f"[red]Failed to start chat session: {e}[/red]")
            raise

    @staticmethod
    def create_client(apikey, version="gemini-2.0-flash"):
        """Create a global Gemini client instance."""
        AsyncGemini.Client = AsyncGemini(apikey, version)

    @staticmethod
    def get_client():
        """Get the global Gemini client instance."""
        if AsyncGemini.Client is None:
            raise ValueError("Gemini client not initialized. Set API key first.")
        return AsyncGemini.Client


@click.command()
@click.option("--apikey", help="Gemini API key (or set in config GEMINI:apikey)")
@click.option("--model", default="gemini-2.0-flash", help="Gemini model to use")
@click.option("--prompt", help="Single prompt instead of interactive chat")
@click.pass_context
async def gemini(ctx, apikey, model, prompt):
    """Chat with Gemini AI or send a single prompt."""
    
    console = _get_console()
    
    # Get API key from parameter or config
    if not apikey:
        try:
            apikey = ctx.obj.get_config(section="GEMINI", config="apikey")
        except KeyError:
            console.print("[red]❌ No API key provided![/red]")
            console.print("Either:")
            console.print("  1. Use --apikey parameter")
            console.print("  2. Set in config: [bold]util config set --section GEMINI --key apikey --value YOUR_KEY[/bold]")
            return
    
    if not apikey:
        console.print("[red]❌ Gemini API key is required[/red]")
        return
    
    try:
        # Create client
        AsyncGemini.create_client(apikey, model)
        client = AsyncGemini.get_client()
        
        if prompt:
            # Single prompt mode
            console.print(f"[bold cyan]🤖 Asking Gemini:[/bold cyan] {prompt}")
            response = await client.request(prompt)
            console.print("[bold blue]Gemini:[/bold blue]")
            Markdown = _get_markdown()
            md = Markdown(response)
            console.print(md)
        else:
            # Interactive chat mode
            await client.chat()
            
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        logger.error(f"Gemini command error: {e}")