from util.logging import logger

import asyncclick as click
from rich.markdown import Markdown
from rich.console import Console

from util.tasks import get_task_warrior_tasks, tw_to_reminders, get_reminder_lists, mark_tw_task_done

@click.group()
@click.pass_context
async def tasks(ctx):
    """Task management commands for TaskWarrior and Reminders integration."""
    logger.info("Tasks command group accessed")

@tasks.command()
@click.pass_context
async def tw(ctx):
    """Show TaskWarrior tasks."""
    get_task_warrior_tasks()

@tasks.command()
@click.option("--uuid", type=str, required=True, help="Task UUID to mark as done")
@click.pass_context
async def tw_done(ctx, uuid):
    """Mark a TaskWarrior task as done."""
    mark_tw_task_done(uuid)

@tasks.command()
@click.pass_context
async def sync(ctx):
    """Sync TaskWarrior tasks to Reminders."""
    tw_to_reminders()

@tasks.command()
@click.pass_context
async def lists(ctx):
    """Show reminder lists."""
    get_reminder_lists()

