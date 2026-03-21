from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
import uuid

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str 

class UserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)