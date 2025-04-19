import click
import logging


# init logging
logger = logging.getLogger(__name__)


@click.command()
@click.pass_context
def hello(ctx):
    click.echo(f"Hello World")
    logger.info("Test Logging")
