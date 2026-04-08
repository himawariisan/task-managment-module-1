import csv
import os
from task_manager.task import Task


class TaskManager:
    def __init__(self, filepath="tasks.txt"):
        self.filepath = filepath
        self.tasks = []
        self._next_id = 1
        self._load_tasks()

    def _load_tasks(self):
        self.tasks = []
        if not os.path.exists(self.filepath):
            return
        with open(self.filepath, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                task = Task.from_dict(row)
                self.tasks.append(task)
        if self.tasks:
            self._next_id = max(t.task_id for t in self.tasks) + 1
