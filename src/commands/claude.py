"""Claude AI chat commands."""
import asyncio
import asyncclick as click
from util.logging import logger

def _get_console():
    """Lazy import Console to improve startup time."""
    from rich.console import Console
    return Console()

def _get_anthropic():
    """Lazy import Anthropic client to improve startup time."""
    import anthropic
    return anthropic

def _get_markdown():
    """Lazy import Markdown to improve startup time.""" 
    from rich.markdown import Markdown
    return Markdown

class AsyncClaude:
    """Async wrapper for Claude AI client."""
    
    Client = None

    def __init__(self, apikey, model="claude-3-5-sonnet-20241022"):
        self.apikey = apikey
        self.model = model
        anthropic = _get_anthropic()
        self.client = anthropic.Anthropic(api_key=self.apikey)

    async def request(self, text):
        """Send a single request to Claude."""
        try:
            # Run the blocking operation in a thread pool
            response = await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: self.client.messages.create(
                    model=self.model,
                    max_tokens=4000,
                    messages=[{"role": "user", "content": text}]
                )
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Error making Claude request: {e}")
            raise

    async def chat(self):
        """Start an interactive chat session with Claude."""
        try:
            console = _get_console()
            console.print("[bold green]🤖 Claude Chat Session Started[/bold green]")
            console.print("[dim]Type 'quit' or 'q' to exit[/dim]")
            console.print("-" * 50)

            # Keep conversation history for context
            conversation = []

            while True:
                try:
                    # Get user input
                    prompt_text = input("\\n👤 You: ").strip()
                    
                    if prompt_text.lower() in ['quit', 'q', 'exit']:
                        console.print("[yellow]Goodbye! 👋[/yellow]")
                        break
                    
                    if not prompt_text:
                        continue
                    
                    console.print("[dim]Thinking...[/dim]")
                    
                    # Add user message to conversation
                    conversation.append({"role": "user", "content": prompt_text})
                    
                    # Send conversation to Claude
                    response = await asyncio.get_event_loop().run_in_executor(
                        None,
                        lambda: self.client.messages.create(
                            model=self.model,
                            max_tokens=4000,
                            messages=conversation
                        )
                    )
                    
                    response_text = response.content[0].text
                    
                    # Add Claude's response to conversation
                    conversation.append({"role": "assistant", "content": response_text})
                    
                    # Display response with rich markdown formatting
                    console.print("[bold blue]Claude:[/bold blue]")
                    Markdown = _get_markdown()
                    md = Markdown(response_text)
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
            logger.error(f"Claude chat session error: {e}")

    @classmethod
    def create_client(cls, apikey, model="claude-3-5-sonnet-20241022"):
        """Create and store a client instance."""
        cls.Client = cls(apikey, model)
    
    @classmethod
    def get_client(cls):
        """Get the stored client instance."""
        return cls.Client


@click.command()
@click.option("--apikey", help="Claude API key (or set via config)")
@click.option("--model", default="claude-3-5-sonnet-20241022", help="Claude model to use")
@click.option("--prompt", help="Single prompt instead of interactive chat")
@click.pass_context
async def claude(ctx, apikey, model, prompt):
    """Chat with Claude AI or send a single prompt."""
    
    console = _get_console()
    
    # Get API key from parameter or config
    if not apikey:
        try:
            apikey = ctx.obj.get_config(section="CLAUDE", config="apikey")
        except KeyError:
            console.print("[red]❌ No API key provided![/red]")
            console.print("Either:")
            console.print("  1. Use --apikey parameter")
            console.print("  2. Set in config: [bold]util config set --section CLAUDE --key apikey --value YOUR_KEY[/bold]")
            return
    
    if not apikey:
        console.print("[red]❌ Claude API key is required[/red]")
        return
    
    try:
        # Create client
        AsyncClaude.create_client(apikey, model)
        client = AsyncClaude.get_client()
        
        if prompt:
            # Single prompt mode
            console.print(f"[bold cyan]🤖 Asking Claude:[/bold cyan] {prompt}")
            response = await client.request(prompt)
            console.print("[bold blue]Claude:[/bold blue]")
            Markdown = _get_markdown()
            md = Markdown(response)
            console.print(md)
        else:
            # Interactive chat mode
            await client.chat()
            
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        logger.error(f"Claude command error: {e}")