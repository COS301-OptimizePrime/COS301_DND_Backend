import datetime
import logging
import os

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer,
                        SmallInteger, String, Table, create_engine, Enum)
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
    uid = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False)
    date_created = Column(
        DateTime,
        nullable=False,
        default=datetime.datetime.now)

    date_updated = Column(
        DateTime,
        nullable=False,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now)

    # User can have many sessions where the user is a dungeon master
    session_dungeon_masters = relationship(
        "Session", back_populates="dungeon_master")

    # User has many sessions
    joined_sessions = relationship("Session", secondary=user_sessions)

    # User has many characters
    characters = relationship(
        "Character", back_populates="creator")

    def __repr__(self):
        return "<User(id='%s', uid='%s', name='%s')>" % (
            self.id, self.uid, self.name)


class Session(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True)
    session_id = Column(String(36), nullable=False, index=True)
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


class Character(Base):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True)
    character_id = Column(String(36), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    date_created = Column(
        DateTime,
        nullable=False,
        default=datetime.datetime.now)
    # Character has only one creator/user
    creator_id = Column(Integer, ForeignKey('users.id'))
    creator = relationship(
        "User", back_populates="characters")

    saving_throws = relationship(
        "SavingThrow",
        uselist=False,
        back_populates="character")

    skills = relationship("Skill", uselist=False, back_populates="character")

    attacks_and_spellcasting = relationship(
        "Attacks_And_Spellcasting",
        uselist=False,
        back_populates="character")
    hitpoints = relationship(
        "Hitpoints",
        uselist=False,
        back_populates="character")

    strength = Column(Integer, nullable=False)
    strength_subscript = Column(Boolean, nullable=False, default=False)

    dexterity = Column(Integer, nullable=False)
    dexterity_subscript = Column(Boolean, nullable=False, default=False)

    constitution = Column(Integer, nullable=False)
    constitution_subscript = Column(Boolean, nullable=False, default=False)

    intelligence = Column(Integer, nullable=False)
    intelligence_subscript = Column(Boolean, nullable=False, default=False)

    wisdom = Column(Integer, nullable=False)
    wisdom_subscript = Column(Boolean, nullable=False, default=False)

    charisma = Column(Integer, nullable=False)
    charisma_subscript = Column(Boolean, nullable=False, default=False)

    character_class = Column(String(100), nullable=False)
    race = Column(String(100), nullable=False)

    xp = Column(Integer, nullable=False)
    alignment = Column(String(200), nullable=False)
    background = Column(String(200), nullable=False)

    inspiration = Column(Integer, nullable=False)
    proficiency_bonus = Column(Integer, nullable=False)


class SavingThrow(Base):
    __tablename__ = 'savingthrows'

    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey('characters.id'))
    character = relationship("Character", back_populates="saving_throws")
    # Saving throws
    strength = Column(Integer, nullable=False)
    strength_proficient = Column(Boolean, nullable=False, default=False)

    dexterity = Column(Integer, nullable=False)
    dexterity_proficient = Column(Boolean, nullable=False, default=False)

    constitution = Column(Integer, nullable=False)
    constitution_proficient = Column(Boolean, nullable=False, default=False)

    intelligence = Column(Integer, nullable=False)
    intelligence_proficient = Column(Boolean, nullable=False, default=False)

    wisdom = Column(Integer, nullable=False)
    wisdom_proficient = Column(Boolean, nullable=False, default=False)

    charisma = Column(Integer, nullable=False)
    charisma_subscript = Column(Boolean, nullable=False, default=False)


class Skill(Base):
    __tablename__ = 'skills'

    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey('characters.id'))
    character = relationship("Character", back_populates="skills")

    acrobatics = Column(Integer, nullable=False)
    acrobatics_proficient = Column(Boolean, nullable=False, default=False)

    animal_handling = Column(Integer, nullable=False)
    animal_handling_proficient = Column(Boolean, nullable=False, default=False)

    arcana = Column(Integer, nullable=False)
    arcana_proficient = Column(Boolean, nullable=False, default=False)

    athletics = Column(Integer, nullable=False)
    athletics_proficient = Column(Boolean, nullable=False, default=False)

    deception = Column(Integer, nullable=False)
    deception_proficient = Column(Boolean, nullable=False, default=False)

    history = Column(Integer, nullable=False)
    history_proficient = Column(Boolean, nullable=False, default=False)

    insight = Column(Integer, nullable=False)
    insight_proficient = Column(Boolean, nullable=False, default=False)

    intimidation = Column(Integer, nullable=False)
    intimidation_proficient = Column(Boolean, nullable=False, default=False)

    investigation = Column(Integer, nullable=False)
    investigation_proficient = Column(Boolean, nullable=False, default=False)

    medicine = Column(Integer, nullable=False)
    medicine_proficient = Column(Boolean, nullable=False, default=False)

    nature = Column(Integer, nullable=False)
    nature_proficient = Column(Boolean, nullable=False, default=False)

    perception = Column(Integer, nullable=False)
    perception_proficient = Column(Boolean, nullable=False, default=False)

    performance = Column(Integer, nullable=False)
    performance_proficient = Column(Boolean, nullable=False, default=False)

    persuasion = Column(Integer, nullable=False)
    persuasion_proficient = Column(Boolean, nullable=False, default=False)

    religion = Column(Integer, nullable=False)
    religion_proficient = Column(Boolean, nullable=False, default=False)

    sleight_of_hand = Column(Integer, nullable=False)
    sleight_of_hand_proficient = Column(Boolean, nullable=False, default=False)

    stealth = Column(Integer, nullable=False)
    stealth_proficient = Column(Boolean, nullable=False, default=False)

    survival = Column(Integer, nullable=False)
    survival_proficient = Column(Boolean, nullable=False, default=False)


class Attacks_And_Spellcasting(Base):
    __tablename__ = 'attacks_and_spellcasting'

    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey('characters.id'))
    character = relationship("Character",
                             back_populates="attacks_and_spellcasting")

    name_1 = Column(String(100), nullable=False)
    name_2 = Column(String(100), nullable=False)
    name_3 = Column(String(100), nullable=False)
    atk_bonus_1 = Column(Integer, nullable=False)
    atk_bonus_2 = Column(Integer, nullable=False)
    atk_bonus_3 = Column(Integer, nullable=False)
    dmage_type_1 = Column(String(100), nullable=False)
    dmage_type_2 = Column(String(100), nullable=False)
    dmage_type_3 = Column(String(100), nullable=False)


class Hitpoints(Base):
    __tablename__ = 'hitpoints'

    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey('characters.id'))
    character = relationship("Character", back_populates="hitpoints")

    armor_class = Column(Integer, nullable=False)
    initiative = Column(Integer, nullable=False)
    speed = Column(Integer, nullable=False)
    current_hitpoints = Column(Integer, nullable=False)
    max_hitpoints = Column(Integer, nullable=False)
    temporary_hitpoints = Column(Integer, nullable=False)
    hitdice = Column(String(100), nullable=False)
