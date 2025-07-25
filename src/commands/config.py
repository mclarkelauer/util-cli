"""Configuration management commands."""
import asyncclick as click
from util.logging import logger
from rich.console import Console
from rich.table import Table

console = Console()

@click.group()
@click.pass_context
async def config(ctx):
    """Configuration management commands."""
    logger.info("Config command group accessed")


@config.command()
@click.pass_context
async def show(ctx):
    """Display current configuration."""
    console.print("[bold cyan]Util CLI Configuration[/bold cyan]")
    console.print("-" * 50)
    
    if hasattr(ctx.obj, 'config') and ctx.obj.config:
        table = Table(title="Configuration Sections")
        table.add_column("Section", style="cyan")
        table.add_column("Key", style="magenta")
        table.add_column("Value", style="green")
        
        for section_name, section_data in ctx.obj.config.items():
            if isinstance(section_data, dict):
                for key, value in section_data.items():
                    # Mask sensitive values
                    display_value = "***" if "key" in key.lower() or "password" in key.lower() else str(value)
                    table.add_row(section_name, key, display_value)
            else:
                table.add_row(section_name, "", str(section_data))
        
        console.print(table)
    else:
        console.print("[yellow]No configuration found or configuration is empty[/yellow]")


@config.command()
@click.option("--section", default="GLOBAL", help="Configuration section")
@click.option("--key", required=True, help="Configuration key")
@click.option("--value", required=True, help="Configuration value")
@click.pass_context
async def set(ctx, section, key, value):
    """Set a configuration value."""
    await ctx.obj.set_config_async(section=section, config=key, value=value)
    await ctx.obj.save_config_async()
    console.print(f"[green]Set {section}:{key} = {value}[/green]")


@config.command()
@click.option("--section", default="GLOBAL", help="Configuration section")
@click.option("--key", required=True, help="Configuration key to get")
@click.pass_context
async def get(ctx, section, key):
    """Get a configuration value."""
    try:
        value = ctx.obj.get_config(section=section, config=key)
        # Mask sensitive values
        display_value = "***" if "key" in key.lower() or "password" in key.lower() else str(value)
        console.print(f"[cyan]{section}:{key}[/cyan] = [green]{display_value}[/green]")
    except KeyError as e:
        console.print(f"[red]Configuration not found: {e}[/red]")


@config.command()
@click.pass_context
async def create(ctx):
    """Create a new configuration file."""
    await ctx.obj.save_config_async()
    console.print(f"[green]Configuration file created at: {ctx.obj.filename}[/green]")