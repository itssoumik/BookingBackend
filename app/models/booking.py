import enum
from typing import TYPE_CHECKING
import uuid
from datetime import date, datetime

from sqlalchemy import Integer, ForeignKey, Date, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base
if TYPE_CHECKING:
    from app.models.user import User
    from app.models.hotel import RoomType, Room

class BookingStatus(str, enum.Enum):
    WAITING = "WAITING"
    PENDING_PAYMENT = "PENDING_PAYMENT"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"

class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    
    #ondelete="RESTRICT" prevents Admin from deleting a RoomType if people are queued for it.
    room_type_id: Mapped[int] = mapped_column(
        ForeignKey("room_types.id", ondelete="RESTRICT"), index=True
    )
    
    #Nullable If status is WAITING 
    room_id: Mapped[int | None] = mapped_column(
        ForeignKey("rooms.id", ondelete="SET NULL"), nullable=True
    )

    check_in: Mapped[date] = mapped_column(Date, nullable=False)
    check_out: Mapped[date] = mapped_column(Date, nullable=False)

    status: Mapped[BookingStatus] = mapped_column(
        SQLEnum(BookingStatus, name="bookingstatus_enum"), 
        default=BookingStatus.WAITING,
        nullable=False
    )

    # This timestamp will be used in the waitlist queue
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="bookings")
    room_type: Mapped["RoomType"] = relationship()
    room: Mapped["Room"] = relationship()