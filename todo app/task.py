from datetime import datetime

class Task:
    def __init__(self, description, urgency="medium"):
        self.description = description
        self.completed = False
        self.created_date = datetime.now()
        self.completed_date = None
        self.urgency = urgency

    def mark_completed(self):
        self.completed = True
        self.completed_date = datetime.now()

    def mark_pending(self):
        self.completed = False
        self.completed_date = None

    def to_dict(self):
        return {
            'description': self.description,
            'completed': self.completed,
            'created_date': self.created_date.isoformat() if self.created_date else None,
            'completed_date': self.completed_date.isoformat() if self.completed_date else None,
            'urgency': self.urgency
        }

    @classmethod
    def from_dict(cls, data):
        task = cls(data['description'], data.get('urgency', 'medium'))
        task.completed = data.get('completed', False)
        task.created_date = datetime.fromisoformat(data['created_date']) if data.get('created_date') else datetime.now()
        task.completed_date = datetime.fromisoformat(data['completed_date']) if data.get('completed_date') else None
        return task

    def __str__(self):
        status = "✅" if self.completed else "🚧"
        return f"{status} {self.description}"
