from fastapi import FastAPI

import os
from pydantic import BaseModel

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext


########## DATABASE ##########

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:admin@database:5432/credentials")
engine = sqlalchemy.create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


########## SCHEMAS - USERS ##########

class UserCreate(BaseModel):
    email:    str
    username: str
    password: str

class UserLogin(BaseModel):
    email:    str
    password: str

    class config:
        from_attributes = True


########## SERVICES - USER_SERVICE ##########

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)
    db_user = Users(
        email=user.email,
        username=user.username,
        password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(Users).filter(Users.email == email).first()
    if not user or not pwd_context.verify(password, user.password):
        return None
    return user


########## MODEL - USERS ##########

class Users(Base):
    __tablename__ = "users"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    username = sqlalchemy.Column(sqlalchemy.String, index=True)
    password = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)
    email    = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)


########## APP ##########

app = FastAPI()

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db, user)
    return db_user

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user.email, user.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials.")
    return {"message": "Successful Login!"}

@app.get("/")
def root():
    return {"message": "Welcome!"}
