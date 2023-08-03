from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    publication_date = Column(DateTime, nullable=False)
    link = Column(String, unique=True, nullable=False)
    author_name = Column(String, nullable=False)
    author_link = Column(String, nullable=False)
    hub_id = Column(Integer, ForeignKey('hubs.id'), nullable=False)
    hub = relationship('Hub', back_populates='articles')


class Hub(Base):
    __tablename__ = 'hubs'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    articles = relationship('Article', back_populates='hub')
