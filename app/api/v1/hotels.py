from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.hotel import Hotel
from app.schemas.hotel_schema import HotelCreate, HotelResponse

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