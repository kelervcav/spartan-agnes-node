from sqlalchemy import Boolean, Column, Integer, String
from .database import Base

class Devices(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    unit = Column(Integer)
    address = Column(Integer)
    status = Column(Boolean, default=False)
