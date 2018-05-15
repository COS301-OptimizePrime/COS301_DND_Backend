import datetime
import logging
import os

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer,
                        SmallInteger, String, Table, create_engine)
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker

import config
import log

Base = declarative_base()


def connect():
    if os.environ['ENV'] == 'prod':
        # logger = logging.getLogger('cos301-DND')
        # logger.debug('Using PostgreSQL!')
        engine = create_engine('postgresql://' +
                               str(config.val['database']['username']) +
                               ':' +
                               str(config.val['database']['password']) +
                               '@' +
                               str(config.val['database']['address']) +
                               ':' +
                               str(config.val['database']['port']) +
                               '/dnd_backend')
    else:
        engine = create_engine(
            'sqlite:///./dnd_backend.db',
            echo=False,
            connect_args={
                'check_same_thread': False})

    Base.metadata.create_all(engine)

    session_factory = sessionmaker(bind=engine)
    session = scoped_session(session_factory)
    return session


user_sessions = Table('usersessions', Base.metadata,
                      Column('users_id', Integer, ForeignKey('users.id')),
                      Column('sessions_id', Integer, ForeignKey('sessions.id'))
                      )


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    uid = Column(String, nullable=False)
    name = Column(String, nullable=False)
    date_created = Column(
        DateTime,
        nullable=False,
        default=datetime.datetime.now)

    #
    session_dungeon_masters = relationship(
        "Session", back_populates="dungeon_master")

    # User has many sessions
    joined_sessions = relationship("Session", secondary=user_sessions)

    def __repr__(self):
        return "<User(id='%s', uid='%s', name='%s')>" % (
            self.id, self.uid, self.name)


class Session(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True)
    session_id = Column(String(36), nullable=False)
    name = Column(String(100), nullable=False)
    date_created = Column(
        DateTime,
        nullable=False,
        default=datetime.datetime.now)
    max_players = Column(SmallInteger, nullable=False)
    full = Column(Boolean, nullable=False, default=False)
    private = Column(Boolean, nullable=False, default=False)

    # Session has only one dungeon master
    dungeon_master_id = Column(Integer, ForeignKey('users.id'))
    dungeon_master = relationship(
        "User", back_populates="session_dungeon_masters")

    # Session has many users
    users_in_session = relationship(
        "User",
        secondary=user_sessions,
        back_populates="joined_sessions")

    users = association_proxy('users_in_session', 'user')

    def __repr__(self):
        return "<Session(id='%s', session_id='%s', name='%s', dungeon_master='%s')>" % (
            self.id, self.session_id, self.name, self.dungeon_master)

# class Party(Base):
# class Combat(Base):
