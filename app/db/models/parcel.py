import uuid

from db.models.base import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ParcelType(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    parcels: Mapped[list["Parcel"]] = relationship(back_populates="parcel_type")


class Parcel(Base):
    parcel_id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False
    )
    name: Mapped[str]
    owner: Mapped[str]
    weight: Mapped[float]
    content_value_usd: Mapped[float]
    delivery_cost_rub: Mapped[float]
    parcel_type: Mapped[str] = mapped_column(
        String(50), ForeignKey("parcel_types.name"), nullable=False
    )
