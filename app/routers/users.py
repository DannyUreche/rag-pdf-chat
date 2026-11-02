from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import UserCreate, UserResponse
from app.repository import UserRepository

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)

    # Verificăm dacă există deja
    existing_user = await repo.get_by_email(user_in.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Creăm utilizatorul
    new_user = await repo.create(user_in)
    return new_user