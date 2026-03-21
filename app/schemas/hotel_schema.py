from pydantic import BaseModel, ConfigDict, EmailStr
from decimal import Decimal
from typing import List, Optional

class HotelCreate(BaseModel):
    name: str
    location: str
    contact_email: EmailStr 

class HotelResponse(BaseModel):
    id: int
    name: str
    location: str
    contact_email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class RoomTypeCreate(BaseModel):
    type_name: str
    base_price: Decimal
    facilities: list[str] = []

class RoomTypeResponse(BaseModel):
    id: int
    hotel_id: int
    type_name: str
    base_price: Decimal
    facilities: list[str] | None

    model_config = ConfigDict(from_attributes=True)

class RoomCreate(BaseModel):
    room_number: str
    is_operational: bool = True

class RoomResponse(BaseModel):
    id: int
    room_type_id: int
    room_number: str
    is_operational: bool

    model_config = ConfigDict(from_attributes=True)