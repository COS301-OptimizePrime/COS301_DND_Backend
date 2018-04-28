from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, DateTime, Integer, SmallInteger, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
import datetime


Base = declarative_base()

def connect():
    engine = create_engine('sqlite:///./dnd_backend.db', echo=False)
    Base.metadata.create_all(engine)
    
    session_factory = sessionmaker(bind=engine)
    session = scoped_session(session_factory)
    return session

association_table = Table('usersessions', Base.metadata,
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
    joined_sessions = relationship("Session", secondary=association_table)

    def __repr__(self):
        return "<User(id='%s', uid='%s', name='%s')>" % (self.id, self.uid, self.name)

class Session(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True)
    session_id = Column(String(36), nullable=False)
    name = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False, default=datetime.datetime.now)
    max_players = Column(SmallInteger, nullable=False)
    
    # Session has only one dungeon master
    dungeon_master_id = Column(Integer, ForeignKey('users.id'))
    dungeon_master = relationship("User", back_populates="session_dungeon_masters")

    # Session has many users
    users_in_session = relationship(
        "User",
        secondary=association_table,
        back_populates="joined_sessions")

    def __repr__(self):
        return "<Session(id='%s', session_id='%s', name='%s', dungeon_master='%s')>" % (self.id, self.session_id, self.name, self.dungeon_master)