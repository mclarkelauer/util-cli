from util.logging import logger

from datetime import datetime
from dataclasses import dataclass
from typing import Any
from pprint import pprint

# Lazy imports for heavy dependencies
def _get_taskw():
    """Lazy import TaskWarrior to improve startup time."""
    from taskw import TaskWarrior
    return TaskWarrior

def _get_remindkit():
    """Lazy import RemindKit to improve startup time."""
    from util.pyremindkit import RemindKit, Priority
    return RemindKit, Priority

def get_task_warrior_tasks():
  TaskWarrior = _get_taskw()
  w = TaskWarrior()
  tasks = w.load_tasks()
  pprint(tasks)
  return tasks

def mark_tw_task_done(uuid):
  TaskWarrior = _get_taskw()
  w = TaskWarrior()
  w.task_done(uuid=uuid)


@dataclass
class Reminder:
    title: Any = None
    due_date: Any = datetime.now()
    notes: Any = None
    priority: Any = None  # Will be set dynamically
    tw_id: Any = None
    uuid: Any = None

def get_reminder_lists():
  RemindKit, Priority = _get_remindkit()
  remind = RemindKit()
  for r in remind.calendars.list():
    pprint(r)

def create_reminders(reminders):
  RemindKit, Priority = _get_remindkit()
  remind = RemindKit()
  default_calendar = remind.calendars.get("Inbox")
  for r in reminders:
    new_reminder = remind.create_reminder(
      title=r.title,
      due_date=r.due_date,
      notes=r.notes,
      priority=r.priority or Priority.HIGH,
      calendar_id=default_calendar.id
    )
    logger.info(f"Created reminder: {new_reminder.title} (ID: {new_reminder.id})")

    if r.uuid:
      mark_tw_task_done(r.uuid)

def convert_tw_to_reminder(tw):
  r = Reminder(
    title = tw['description'],
    due_date = None,
    priority = None,
    tw_id = tw['id'],
    uuid = tw['uuid']
  )
  return r

def tw_to_reminders():
  tws = get_task_warrior_tasks()
  reminders = []
  for tw in tws['pending']:
    reminders.append(convert_tw_to_reminder(tw))
  create_reminders(reminders)

