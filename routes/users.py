# Author: Manzoor Hussain

from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import AsyncSessionLocal
from models import User
from schemas import UserCreate, UserOut, UserUpdate

router = APIRouter()


# Dependency to get DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@router.post("/users", response_model=UserOut)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)) -> User:
    # Check if user already exists
    result = await db.execute(select(User).where(User.email == user.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered.")

    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)) -> User:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return user


@router.get("/users/", response_model=List[UserOut])
async def get_users(db: AsyncSession = Depends(get_db)) -> List[User]:
    result = await db.execute(select(User))
    users = result.scalars().all()

    return list(users)


@router.put("/users/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user_update: UserUpdate, db: AsyncSession = Depends(get_db)) -> User:
    result = await db.execute(select(User).where(User.id == user_id))
    found_user = result.scalar_one_or_none()
    if not found_user:
        raise HTTPException(status_code=404, detail="User not found.")

    if user_update.name is not None:
        found_user.name = user_update.name
    if user_update.email is not None:
        found_user.email = user_update.email

    await db.commit()
    await db.refresh(found_user)
    return found_user


@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    await db.delete(user)
    await db.commit()

    return {"message": f"User with id {user_id} deleted successfully."}
