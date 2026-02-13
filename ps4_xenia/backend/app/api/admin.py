from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.core.database import get_session
from app.models.models import Asset, User, UserRole

router = APIRouter()

# --- Assets ---
@router.post("/assets/", response_model=Asset)
def create_asset(asset: Asset, session: Session = Depends(get_session)):
    session.add(asset)
    session.commit()
    session.refresh(asset)
    return asset

@router.get("/assets/", response_model=List[Asset])
def read_assets(session: Session = Depends(get_session)):
    assets = session.exec(select(Asset)).all()
    return assets

# --- Users ---
@router.post("/users/", response_model=User)
def create_user(user: User, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.get("/users/all", response_model=List[User])
def read_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()

@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: str, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
