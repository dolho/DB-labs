from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text


Base = declarative_base()


class Tag(Base):
    __tablename__ = 'Tag'
    id = Column(Integer, primary_key=True)
    references = Column(Integer)
    tag = Column(Text)
