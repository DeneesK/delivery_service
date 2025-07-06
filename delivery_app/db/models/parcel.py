import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base


class ParcelType(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
    parcels: Mapped[list["Parcel"]] = relationship(back_populates="parceltype")


class Parcel(Base):
    parcel_id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(256))
    owner: Mapped[str] = mapped_column(String(256))
    weight: Mapped[float]
    content_value_usd: Mapped[float]
    delivery_cost_rub: Mapped[float] = mapped_column(nullable=True)
    parcel_type: Mapped[str] = mapped_column(
        String(256),
        ForeignKey("parceltype.name"),
        nullable=False,
    )
    company_id: Mapped[int | None] = mapped_column(ForeignKey("companies.id"), nullable=True)

    company = relationship("Company", back_populates="parcels")
    parceltype: Mapped["ParcelType"] = relationship(back_populates="parcels")
