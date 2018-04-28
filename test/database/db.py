from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, DateTime, Integer, SmallInteger, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
import datetime


Base = declarative_base()

def connect():
    engine = create_engine('sqlite:///./dnd_backend.db', echo=True)
    Base.metadata.create_all(engine)
    
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    return session

association_table = Table('usersessionassociation', Base.metadata,
    Column('users_id', Integer, ForeignKey('users.id')),
    Column('sessions_id', Integer, ForeignKey('sessions.id'))
)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    uid = Column(String, nullable=False)
    name = Column(String, nullable=False)
    date_created = Column(DateTime, nullable=False, default=datetime.datetime.now)
    sessions = relationship("Session", secondary=association_table, back_populates="users")

    def __repr__(self):
        return "<User(id='%s', uid='%s', name='%s')>" % (self.id, self.uid, self.name)

class Session(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True)
    session_id = Column(String(36), nullable=False)
    name = Column(String(100), nullable=False)
    dungeon_master = Column(Integer, ForeignKey("users.id"), nullable=False)
    date_created = Column(DateTime, nullable=False, default=datetime.datetime.now)
    max_players = Column(SmallInteger, nullable=False)
    users = relationship(
        "User",
        secondary=association_table,
        back_populates="sessions")

    def __repr__(self):
        return "<Session(id='%s', session_id='%s', name='%s', dungeon_master='%s')>" % (self.id, self.session_id, self.name, self.dungeon_master)

def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.iteritems() if not isinstance(v, ClauseElement))
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        return instance, True