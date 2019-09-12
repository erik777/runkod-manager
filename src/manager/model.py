from sqlalchemy import (Column, String, DateTime, Integer, SmallInteger)
from sqlalchemy.ext.declarative import declarative_base

from manager.util import now_utc

Base = declarative_base()

__all__ = ['Base', 'State', 'Domain']


class State(Base):
    __tablename__ = 'state'

    id = Column('id', String, nullable=False, primary_key=True)
    project_since_time = Column('project_since_time', String)
    config_checksum = Column('config_checksum', String)


class Domain(Base):
    __tablename__ = 'domains'

    name = Column('name', String, nullable=False, primary_key=True)

    cert = Column('cert_status', SmallInteger, nullable=False, default=0)

    ip_err_count = Column('ip_err_count', Integer, nullable=False, default=0)

    stopped = Column('stopped', SmallInteger, nullable=False, default=0)

    created = Column('created', DateTime(timezone=True), nullable=False, default=now_utc)

    next_check = Column('next_check', DateTime(timezone=True), nullable=False, default=now_utc)

    def __repr__(self):
        return '<Domain {}>'.format(self.name)
