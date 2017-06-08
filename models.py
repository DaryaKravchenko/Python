from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

Base = declarative_base()


class Users(Base):
    __tablename__ = 'Users'

    userID = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    geolocationState = Column(Integer, nullable=False)
    work = relationship("Works", backref='users', cascade="save-update, merge, delete")


class Works(Base):
    __tablename__ = 'Works'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    userID = Column(Integer, ForeignKey('Users.userID', onupdate="CASCADE", ondelete="CASCADE"))
