from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Settings(Base):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ip_address = Column(String)
    subnet_mask = Column(String)
    gateway = Column(String)
    dns = Column(String)
    longitude = Column(String)
    latitude = Column(String)
