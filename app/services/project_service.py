from datetime import datetime

from app.models.exceptions import ServiceError
from app.models.project import Project

projects = [Project('1', 'Project 1', datetime.now()), Project('2', 'Project 2', datetime.now())]


def find_all() -> [Project]:
    return [project.to_dict() for project in projects]


def find_one(uuid: str = None, name: str = None) -> Project:
    if uuid is None and name is None:
        raise ServiceError
    if uuid in [project.uuid for project in projects]:
        return [project for project in projects if project.uuid == uuid][0]
    raise ServiceError
