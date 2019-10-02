from sqlalchemy import (Column, String, DateTime, Integer, SmallInteger, Binary)
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

    id = Column('id', Integer, nullable=False, primary_key=True)

    name = Column('name', String, nullable=False, unique=True)

    ip_errs = Column('ip_errs', Integer, nullable=False, default=0)

    next_ip_check = Column('next_ip_check', DateTime(timezone=True), nullable=False, default=now_utc)

    stopped = Column('stopped', SmallInteger, nullable=False, default=0)

    cert_status = Column('cert_status', SmallInteger, nullable=False, default=0)

    cert_file = Column('cert_file', Binary)

    cert_key_file = Column('cert_key_file', Binary)

    cert_date = Column('cert_date', DateTime(timezone=True))

    created = Column('created', DateTime(timezone=True), nullable=False, default=now_utc)

    def __repr__(self):
        return '<Domain {}>'.format(self.name)
