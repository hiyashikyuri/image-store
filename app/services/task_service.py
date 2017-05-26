from datetime import datetime

from app.models.exceptions import ServiceError
from app.models.task import Task

tasks = [Task('1', 'Task 1', datetime.now()), Task('2', 'Task 2', datetime.now())]


def find_all() -> [Task]:
    return [task.to_dict() for task in tasks]


def find_one(uuid: str = None, name: str = None) -> Task:
    if uuid is None and name is None:
        raise ServiceError
    if uuid in [task.uuid for task in tasks]:
        return [task for task in tasks if task.uuid == uuid][0]
    raise ServiceError
