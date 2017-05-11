import os
import sys
import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine


Base = declarative_base()


class Users(Base):
    """creates a user's table"""
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

    def __repr__(self):
        return 'username{} email{}'.format(self.user_name,self.email)


class Buckectlist(Base):
    """creates Buckectlist tables"""
    __tablename__ = "bucketList"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey('user.id'), nullable=False)
    item = Column(String, nullable=False)
    created_date = Column(DateTime, nullable=False)
    user = relationship('Users')
    modified_date = Column(DateTime, nullable=False)

class Item(Base):
    """creates Items tables"""
    __tablename__ = "Items"

    id = Column(Integer, foreign_key=True, autoincrement=True)
    buckectlist_id = Column(ForeignKey('bucketList.id'), nullable=False)
    name = Column(String, nullable=False)
    created_date = Column(DateTime, nullable=False)
    modified_date = Column(DateTime, nullable=False)
    buckectlist = relationship('Buckectlist')
    Done = Column(Boolean)

class DatabaseCreator(object):
    """creating database connection to object"""
    def __init__(self, db_name=None):
        self.db_name = db_name + '.db'
        self.engine = create_engine('sqlite:///' + self.db_name)
        Base.metadata.create_all(self.engine)
        session_maker = sessionmaker(bind=self.engine)
        self.session = session_maker()