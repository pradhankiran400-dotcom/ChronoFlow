from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    name: str
    picture: Optional[str] = None
    google_id: Optional[str] = None
    credential: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    picture: Optional[str] = None
    google_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
