import click
import logging

# utils
import util.logging as log

# command
from commands.hello import hello
from commands.scrape import scrape

@click.group()
@click.option('--log-level', default='ERROR')
@click.pass_context
def cli(ctx, log_level):
    ctx.ensure_object(dict)
    ctx.obj['LOG_LEVEL'] = log_level
    log.init_logging(log_level)


cli.add_command(hello)
cli.add_command(scrape)
