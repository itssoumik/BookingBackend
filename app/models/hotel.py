from decimal import Decimal
from typing import List
from sqlalchemy import String, Integer, ForeignKey, Boolean, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from app.core.database import Base

class Hotel(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    location: Mapped[str] = mapped_column(String, nullable=False)
    contact_email: Mapped[str] = mapped_column(String, nullable=False)
    
    # One-to-Many: A hotel has many room types
    room_types: Mapped[List["RoomType"]] = relationship(
        back_populates="hotel", cascade="all, delete-orphan"
    )


class RoomType(Base):
    __tablename__ = "room_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id", ondelete="CASCADE"), index=True)
    type_name: Mapped[str] = mapped_column(String, nullable=False)
    base_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    
    # JSONB is for storeing lists like ["WiFi", "AC"] and also query them 
    facilities: Mapped[list | dict | None] = mapped_column(JSONB, nullable=True)

    # Relationships
    hotel: Mapped["Hotel"] = relationship(back_populates="room_types")
    rooms: Mapped[List["Room"]] = relationship(
        back_populates="room_type", cascade="all, delete-orphan"
    )

class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    room_type_id: Mapped[int] = mapped_column(ForeignKey("room_types.id", ondelete="CASCADE"), index=True)
    
    room_number: Mapped[str] = mapped_column(String, nullable=False)
    
    is_operational: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")

    # Relationships
    room_type: Mapped["RoomType"] = relationship(back_populates="rooms")