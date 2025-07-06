from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.models.base import Base


class Company(Base):

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)

    parcels = relationship("Parcel", back_populates="company")
