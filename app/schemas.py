from pydantic import BaseModel, EmailStr
from datetime import datetime


# --- Modele pentru User ---
class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: str
    created_at: datetime

    # Permite conversia automată din modelele SQLAlchemy
    class Config:
        from_attributes = True


# --- Modele pentru Autentificare ---
class Token(BaseModel):
    access_token: str
    token_type: str