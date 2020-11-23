from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text


Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'

    email = Column(Text, primary_key=True)
    nickname = Column(Text)
    rating = Column(Integer)
    registered_at = Column(Date)
    role = Column(Text)
    login = Column(Text)
    password = Column(Text)