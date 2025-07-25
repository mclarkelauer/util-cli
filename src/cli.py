<<<<<<< HEAD
import click

# utils
import util.logging as log

from util.config import Config

# command
from commands.scrape import scrape
from commands.config import config
from commands.gemini import gemini
from commands.tasks import tasks 

from util.config import config_file
"""Main CLI module for the util package."""
import asyncclick as click
import ccl

import util.logging as log
from util.config import Config, CONFIG_FILE

# Import commands from commands directory
try:
    from commands.config import config
except ImportError:
    config = None

try:
    from commands.gemini import gemini
except ImportError:
    gemini = None

try:
    from commands.scrape import scrape
except ImportError:
    scrape = None

try:
    from commands.demo import demo
except ImportError:
    demo = None

@click.group()
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


# Register commands from commands directory using standard click registration
if config:
    cli.add_command(config)
if gemini:
    cli.add_command(gemini)
if scrape:
    cli.add_command(scrape)
if demo:
    cli.add_command(demo)

# Register dynamic commands from out_of_repo_commands using ccl
# Note: There's a compatibility issue between ccl and asyncclick
# For now, ccl loading is disabled. External commands should be added to src/commands/
out_of_repo_path = Path(__file__).parent.parent / 'out_of_repo_commands'
# TODO: Fix ccl + asyncclick compatibility
# if out_of_repo_path.is_dir():
#     ccl.register_commands(cli, out_of_repo_path)
