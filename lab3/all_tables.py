from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from datetime import date



Base = declarative_base()


class Answer(Base):
    __tablename__ = 'Answer'

    id = Column(Integer, primary_key=True)
    text = Column(Text)
    rating = Column(Integer)
    user_email = Column(Text, ForeignKey('Users.email'))
    question_id = Column(Integer, ForeignKey('Question.id'))
    question = relationship("Question")
    user = relationship("User")

    def __init__(self, text, rating, user_email, question_id):
        self.text = text
        self.rating = rating
        self.user_email = user_email
        self.question_id = question_id


class Question(Base):
    __tablename__ = 'Question'

    id = Column(Integer, primary_key=True)
    text = Column(Text)
    rating = Column(Integer)
    user_email = Column(Text, ForeignKey("Users.email"))
    date = Column(Date)
    answer = relationship("Answer", cascade="all, delete-orphan")

    def __init__(self, text, rating, user_email):
        self.text = text
        self.rating = rating
        self.user_email = user_email
        self.date = date.today()


class Tag(Base):
    __tablename__ = 'Tag'
    id = Column(Integer, primary_key=True)
    references = Column(Integer)
    tag = Column(Text)

    def __init__(self, refernces, tag):
        self.references = refernces
        self.tag = tag

class User(Base):
    __tablename__ = 'Users'

    email = Column(Text, primary_key=True)
    nickname = Column(Text)
    rating = Column(Integer)
    registered_at = Column(Date)
    role = Column(Text)
    login = Column(Text)
    password = Column(Text)
    answer = relationship("Answer", cascade="all, delete-orphan")
    question = relationship("Question", cascade="all, delete-orphan")

    def __init__(self, email, nickname, rating, role, login, password):
        self.rating = rating
        self.role = role
        self.nickname = nickname
        self.login = login
        self.password = password
        self.email = email
        self.registered_at = date.today()


Question_Tag = Table('Question/Tag', Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('question_id', Integer, ForeignKey('Question.id')),
    Column('tag_id', Integer, ForeignKey('Tag.id'))
)
