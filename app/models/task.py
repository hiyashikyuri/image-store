from datetime import datetime


class Task:
    def __init__(self, uuid: str, name: str, created_at: datetime):
        self.uuid = uuid
        self.name = name
        self.createdAt = created_at

    def __repr__(self, *args, **kwargs):
        return str(self.to_dict())

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'name': self.name,
            'created_at': self.createdAt.isoformat()
        }
