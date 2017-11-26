import os
import sys
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Deal(Base):
    __tablename__ = 'deals'
    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    url = Column(String(250), nullable=False)

    def __repr__(self):
        return '<Title %r>' % self.title

class Sent(Base):
    __tablename__ = "sent"
    id = Column(Integer, ForeignKey("deals.id"), primary_key=True)
    deal = relationship(Deal)

engine = create_engine('sqlite:///vinyldeals/db/deals.db')

Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()
