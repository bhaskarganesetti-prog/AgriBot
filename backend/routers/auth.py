from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import UserProfile
from schemas import UserRegistration, UserLogin
import os

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
def register_user(data: UserRegistration, db: Session = Depends(get_db)):
    # Check if email is already registered
    existing_user = db.query(UserProfile).filter(UserProfile.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered.")
    
    if data.password != data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match.")

    new_user = UserProfile(
        name=data.name,
        email=data.email,
        password=data.password,
        confirm_password=data.confirm_password,
        mobile=data.mobile,
        status="waiting"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Registration successful. Please wait for admin approval.", "user_id": new_user.id}

@router.post("/login")
def login_user(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email not registered.")
    
    if user.status.lower() == 'blocked':
        raise HTTPException(status_code=403, detail="Your account is blocked. Please contact admin.")
    
    if user.status.lower() != 'activated':
        raise HTTPException(status_code=403, detail="Account not active. Please wait for admin approval.")

    if user.password != data.password:
        raise HTTPException(status_code=401, detail="Invalid password.")
    
    return {"message": "Login successful", "name": user.name, "email": user.email, "id": user.id}
