import click
import logging

# utils
import util.logging as log

from util.config import Config

# command
from commands.scrape import scrape
from commands.config import config
from commands.gemini import gemini

from util.config import config_file 

import ccl
import pathlib

@click.group()
@click.option(
    '-c', '--config',
    type         = click.Path(dir_okay=False),
    default      = config_file,
    callback     = Config.click_callback,
    is_eager     = True,
    expose_value = False,
    help         = 'Read option defaults from the specified config file',
    show_default = True,
)
@click.option('--log-level', default='ERROR')
@click.pass_context
def cli(ctx, log_level):
    ctx.ensure_object(Config)
    ctx.obj.set_config(config='log_level',value=log_level)
    log.init_logging(log_level)

cli.add_command(gemini)
cli.add_command(config)
cli.add_command(scrape)


path_to_commands = pathlib.Path(__file__, "..", "out_of_repo_commands")
ccl.register_commands(cli, path_to_commands)
