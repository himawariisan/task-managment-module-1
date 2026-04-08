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

    def _save_tasks(self):
        fieldnames = [
            "task_id", "description", "priority", 
            "creation_date", "completed"
        ]
        with open(self.filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for task in self.tasks:
                writer.writerow(task.to_dict())

    def add_task(self, description, priority):
        if not (1 <= priority <= 5):
            raise ValueError("Priority must be between 1 and 5.")
        task = Task(self._next_id, description, priority)
        self._next_id += 1
        self.tasks.append(task)
        self._save_tasks()
        return task

    def delete_task(self, task_id):
        task = self._find_task(task_id)
        if task is None:
            raise KeyError(f"Task with ID {task_id} not found.")
        self.tasks.remove(task)
        self._save_tasks()

    def complete_task(self, task_id):
        task = self._find_task(task_id)
        if task is None:
            raise KeyError(f"Task with ID {task_id} not found.")
        task.mark_as_completed()
        self._save_tasks()
        return task

    def complete_and_remove_task(self, task_id):
        task = self._find_task(task_id)
        if task is None:
            raise KeyError(f"Task with ID {task_id} not found.")
        task.mark_as_completed()
        self.tasks.remove(task)
        self._save_tasks()
        return task

    def list_tasks(self, sort_by="priority"):
        if sort_by == "priority":
            return sorted(self.tasks, key=lambda t: t.priority)
        elif sort_by == "creation_date":
            return sorted(self.tasks, key=lambda t: t.creation_date)
        return list(self.tasks)

    def _find_task(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None
