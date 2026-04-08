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

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "description": self.description,
            "priority": self.priority,
            "creation_date": self.creation_date,
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, data):
        task = cls(
            int(data["task_id"]),
            data["description"],
            int(data["priority"])
        )
        task.creation_date = data["creation_date"]
        task.completed = data["completed"] == "True" or data["completed"] is True
        return task
    
    def __str__(self):
        status = "Completed" if self.completed else "Pending"
        return (
            f"Task ID: {self.task_id}\n"
            f"Description: {self.description}\n"
            f"Priority: {self.priority}\n"
            f"Created: {self.creation_date}\n"
            f"Status: {status}"
        )
