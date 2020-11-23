from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text


Base = declarative_base()


class Question(Base):
    __tablename__ = 'Question'

    id = Column(Integer, primary_key=True)
    text = Column(Text)
    rating = Column(Integer)
    user_email = Column(Text, ForeignKey=True)
    date = Column(Date, ForeignKey=True)