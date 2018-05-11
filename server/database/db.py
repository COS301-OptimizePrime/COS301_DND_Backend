from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, DateTime, Integer, SmallInteger, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.ext.associationproxy import association_proxy
import datetime

import os

import logging
import log

Base = declarative_base()

def connect():
    if os.environ['ENV'] == 'prod':
        #logger = logging.getLogger('cos301-DND')
        #logger.debug('Using PostgreSQL!')
        engine = create_engine('postgresql://dnd_backend:dnd_backend@localhost:5432/dnd_backend')
    else:
        engine = create_engine('sqlite:///./dnd_backend.db', echo=False, connect_args={'check_same_thread':False})

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
    date_created = Column(DateTime, nullable=False, default=datetime.datetime.now)

    # 
    session_dungeon_masters = relationship("Session", back_populates="dungeon_master")
    
    # User has many sessions
    joined_sessions = relationship("Session", secondary=user_sessions)

    def __repr__(self):
        return "<User(id='%s', uid='%s', name='%s')>" % (self.id, self.uid, self.name)

class Session(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True)
    session_id = Column(String(36), nullable=False)
    name = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False, default=datetime.datetime.now)
    max_players = Column(SmallInteger, nullable=False)
    full = Column(Boolean, nullable=False, default=False)
    private = Column(Boolean, nullable=False, default=False)

    # Session has only one dungeon master
    dungeon_master_id = Column(Integer, ForeignKey('users.id'))
    dungeon_master = relationship("User", back_populates="session_dungeon_masters")

    # Session has many users
    users_in_session = relationship(
        "User",
        secondary=user_sessions,
        back_populates="joined_sessions")

    users = association_proxy('users_in_session','user')

    def __repr__(self):
        return "<Session(id='%s', session_id='%s', name='%s', dungeon_master='%s')>" % (self.id, self.session_id, self.name, self.dungeon_master)

#class Party(Base):
#class Combat(Base):
