import uuid
import bcrypt
from fastapi import APIRouter, HTTPException
from models.user import User
from pydantic_schemas.user_create import UserCreate
from database import db
from pydantic_schemas.user_login import UserLogin
import jwt


router = APIRouter()

@router.post("/signup")
def signup_user(user: UserCreate):
    user_db = db.query(User).filter(User.email == user.email).first()

    if user_db:
        raise HTTPException(400, 'User with the same email already exists!')
    
    hashedpw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    user_db = User(id=str(uuid.uuid1()), email = user.email, name = user.name, password = hashedpw)

    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

@router.post("/login")
def login_user(user: UserLogin):
    user_db = db.query(User).filter(User.email == user.email).first()

    if not user_db:
        raise HTTPException(400, 'User with this email soes not exist!')
    
    is_match = bcrypt.checkpw(user.password.encode(), user_db.password)

    if not is_match:
        raise HTTPException(400, 'Wrong password!')
    
  

    return {'user': user_db}