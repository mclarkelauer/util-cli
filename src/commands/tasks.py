from util.logging import logger

import click
from rich.markdown import Markdown
from rich.console import Console

from util.tasks import get_task_warrior_tasks, tw_to_reminders, get_reminder_lists

@click.group()
@click.pass_context
def tasks(ctx):
    logger.info("Test Logging")



@tasks.command
@click.pass_context
def taskwarrior(ctx):
  get_task_warrior_tasks()

@tasks.command
@click.pass_context
def sync(ctx):
  tw_to_reminders()

@tasks.command
@click.pass_context
def lists(ctx):
  get_reminder_lists()

