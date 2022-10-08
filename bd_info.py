import sys
# для настройки баз данных
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import create_engine
from bd import global_init


Base = declarative_base()


class User(Base, SerializerMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    role = Column(String)
    login = Column(String, unique=True)
    password = Column(String)
    name = Column(String)
    avatar_url = Column(String)
    surname = Column(String)
    team_id = Column(String)
    public_key = Column(String)
    private_key = Column(String)
    lvl = Column(Integer)

engine = create_engine(f'sqlite:///nodes.sqlite3')

Base.metadata.create_all(engine)
