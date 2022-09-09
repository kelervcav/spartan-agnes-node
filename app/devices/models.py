from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Devices(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    unit = Column(Integer)
    address = Column(Integer)
    status = Column(Boolean, default=False)

    commands = relationship("Commands", back_populates="device")

class Commands(Base):
    __tablename__ = "commands"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    address = Column(String)
    value = Column(String)
    device_id = Column(Integer, ForeignKey("devices.id"))

    device = relationship("Devices", back_populates="commands")