import click
import logging
from util.logging import logger

import IPython


@click.group()
@click.pass_context
def config(ctx):
    logger.info("Test Logging")


@config.command()
@click.pass_context
def show(ctx):
    click.echo(f"Util Cli Config Structure")
    click.echo("--------------------------")
    click.echo(ctx.obj)
    click.echo("--------------------------")


@config.command()
@click.pass_context
def create(ctx):
    click.echo("create")


@config.command()
@click.pass_context
def set(ctx):
    click.echo("set")
