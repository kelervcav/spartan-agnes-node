from sqlalchemy import Boolean, Column, Integer, String
from .database import Base

class Devices(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    unit = Column(Integer)
    address = Column(Integer)
    status = Column(Boolean, default=False)


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    password = Column(String)
