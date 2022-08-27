from sqlalchemy import Boolean, Column, Integer, String
from .database import Base

class Devices(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer)
    size = Column(Integer)
    label = Column(String)
    price = Column(Integer)
    status = Column(Boolean, default=False)
