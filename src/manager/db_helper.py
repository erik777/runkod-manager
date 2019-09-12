from sqlalchemy.orm.session import Session
from typing import Union

from manager.model import State


def set_project_since_time(session: Session, time: float):
    s = session.query(State).first()
    s.project_since_time = time


def get_project_since_time(session: Session) -> Union[float, None]:
    s = session.query(State).first()

    if s.project_since_time is not None:
        return float(s.project_since_time)

    return None
