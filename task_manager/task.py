from datetime import datetime


class Task:
    def __init__(self, task_id, description, priority):
        self.task_id = task_id
        self.description = description
        self.priority = priority
        self.creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.completed = False
    
    def mark_as_completed(self):
        self.completed = True
