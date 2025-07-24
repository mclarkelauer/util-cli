from util.logging import logger

import click
from rich.markdown import Markdown
from rich.console import Console

from util.tasks import get_task_warrior_tasks, tw_to_reminders, get_reminder_lists, mark_tw_task_done
@click.group()
@click.pass_context
def tasks(ctx):
    logger.info("Test Logging")

@tasks.command
@click.pass_context
def tw(ctx):
  get_task_warrior_tasks()

@tasks.command
@click.option("--uuid", type=str)
@click.pass_context
def tw_done(ctx, uuid):
  mark_tw_task_done(uuid)

@tasks.command
@click.pass_context
def sync(ctx):
  tw_to_reminders()

@tasks.command
@click.pass_context
def lists(ctx):
  get_reminder_lists()

