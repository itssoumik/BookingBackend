from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
import uuid

class BookingCreate(BaseModel):
    room_type_id: int
    check_in: date
    check_out: date

class BookingResponse(BaseModel):
    id: int
    user_id: uuid.UUID
    room_type_id: int
    room_id: int | None  
    check_in: date
    check_out: date
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)