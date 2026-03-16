from ._anvil_designer import Form1Template
from anvil import *

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    def add_task(description):
      app_tables.tasks.add_row(description=description,
                               completed=False,
                               created=datetime.now())

def get_all_tasks():
  # Return all tasks, newest first
  return app_tables.tasks.search(tables.order_by("created", ascending=False))

def toggle_task(task_row, completed):
  task_row['completed'] = completed

def delete_task(task_row):
  task_row.delete()
