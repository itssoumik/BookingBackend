from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.hotel import Hotel, RoomType, Room
from app.schemas.hotel_schema import HotelCreate, HotelResponse, RoomTypeCreate, RoomTypeResponse, RoomCreate, RoomResponse

router = APIRouter()

@router.post("/", response_model=HotelResponse, status_code=status.HTTP_201_CREATED)
def create_hotel(hotel_in: HotelCreate, db: Session = Depends(get_db)):
    """
    Create a new hotel. (Admin Only - but we will add the Admin check later)
    """

    new_hotel = Hotel(
        name=hotel_in.name,
        location=hotel_in.location,
        contact_email=hotel_in.contact_email
    )
    
    db.add(new_hotel)
    db.commit()

    db.refresh(new_hotel)

    return new_hotel


@router.post("/{hotel_id}/room-types", response_model=RoomTypeResponse, status_code=status.HTTP_201_CREATED)
def create_roomType(roomType_in: RoomTypeCreate, hotel_id:int, db: Session = Depends(get_db)):
    # Verify the hotel actually exists first
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
    
    new_roomType= RoomType (
        hotel_id=hotel_id,
        type_name=roomType_in.type_name,
        base_price=roomType_in.base_price,
        facilities=roomType_in.facilities
    )
    db.add(new_roomType)
    db.commit()
    db.refresh(new_roomType)
    
    return new_roomType


@router.post("/{hotel_id}/room-types/{room_type_id}/rooms", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room(room_in: RoomCreate,hotel_id:int, room_type_id:int, db: Session = Depends(get_db)):
    # Verify the roomType actually exists first
    roomType = db.query(RoomType).filter(RoomType.id == room_type_id, RoomType.hotel_id==hotel_id).first()
    if not roomType:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room Type not found or doesn't belong to this hotel")
    
    new_room= Room (
        room_type_id=room_type_id,
        room_number=room_in.room_number,
        is_operational=room_in.is_operational
    )
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    
    return new_room
    