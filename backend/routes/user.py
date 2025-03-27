from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.dependencies.database import get_db
from backend.schemas.users import UserCreate, UserLogin
from backend.services.user_service import create_user, authenticate_user

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db, user)
    return db_user

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user.email, user.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials.")
    return {"message": "Login successful!"}

