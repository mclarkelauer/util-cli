"""Main CLI module for the util package."""
import asyncio
from pathlib import Path

import asyncclick as click

import util.logging as log
from util.config import Config, CONFIG_FILE

class LazyGroup(click.Group):
    """A group that lazy-loads commands to improve startup time."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._command_modules = {
            'config': 'commands.config',
            'gemini': 'commands.gemini',
            'claude': 'commands.claude',
            'scrape': 'commands.scrape',
            'demo': 'commands.demo',
            'tasks': 'commands.tasks',
        }
    
    def get_command(self, ctx, cmd_name):
        """Lazy load command when first accessed."""
        if cmd_name in self._command_modules:
            try:
                module_name = self._command_modules[cmd_name]
                module = __import__(module_name, fromlist=[cmd_name])
                return getattr(module, cmd_name)
            except (ImportError, AttributeError):
                return None
        return super().get_command(ctx, cmd_name)
    
    def list_commands(self, ctx):
        """List all available commands."""
        return list(self._command_modules.keys())


@click.group(cls=LazyGroup)
@click.option(
    "-c",
    "--config",
    type=click.Path(dir_okay=False),
    default=CONFIG_FILE,
    callback=Config.click_callback,
    is_eager=True,
    expose_value=False,
    help="Read option defaults from the specified config file",
    show_default=True,
)
@click.option("--log-level", default="ERROR")
@click.pass_context
async def cli(ctx, log_level):
    """Main CLI entry point."""
    ctx.ensure_object(Config)
    await ctx.obj.set_config_async(config="log_level", value=log_level)
    await log.init_logging_async(log_level)

# Dynamic command loading from out_of_repo_commands disabled for performance
# Commands should be added to src/commands/ and registered in LazyGroup
