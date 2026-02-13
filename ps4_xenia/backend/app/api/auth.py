"""
Authentication API endpoints.
Handles user registration, login, logout, and token refresh.
"""
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlmodel import Session, select
from pydantic import BaseModel, EmailStr
from app.core.database import get_session
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user
)
from app.models.models import User, LearningStyle

router = APIRouter()
security = HTTPBearer()


# --- Request/Response Models ---

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    department: Optional[str] = None
    role: str = "Employee"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    department: Optional[str]
    is_admin: bool
    preferred_learning_style: str
    current_skills: list
    target_skills: list


# --- Endpoints ---

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserRegister, session: Session = Depends(get_session)):
    """
    Register a new user account.
    
    WHEN an Employee provides valid registration data,
    THE Auth_Service SHALL create a new User account and issue session tokens.
    """
    # Check if user already exists
    existing_user = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        role=user_data.role,
        department=user_data.department,
        is_active=True,
        is_admin=False
    )
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    # Generate tokens
    access_token = create_access_token(data={"sub": str(new_user.id)})
    refresh_token = create_refresh_token(data={"sub": str(new_user.id)})
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, session: Session = Depends(get_session)):
    """
    Authenticate user and issue session tokens.
    
    WHEN an Employee provides valid credentials,
    THE Auth_Service SHALL authenticate the Employee and issue a session token.
    
    WHEN an Employee provides invalid credentials,
    THE Auth_Service SHALL reject the authentication attempt and return an error message.
    """
    # Find user by email
    user = session.exec(
        select(User).where(User.email == credentials.email)
    ).first()
    
    # Verify user exists and password is correct
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    session.add(user)
    session.commit()
    
    # Generate tokens
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(refresh_token: str, session: Session = Depends(get_session)):
    """
    Refresh an expired access token using a valid refresh token.
    
    WHEN a session token expires,
    THE Platform SHALL require re-authentication before allowing further access.
    """
    try:
        payload = decode_token(refresh_token)
        
        # Verify token type
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        # Verify user exists and is active
        user = session.get(User, user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        # Generate new tokens
        new_access_token = create_access_token(data={"sub": str(user.id)})
        new_refresh_token = create_refresh_token(data={"sub": str(user.id)})
        
        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token
        )
    
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user's profile.
    
    WHEN an authenticated Employee requests a protected resource,
    THE Backend_Service SHALL validate the session token before granting access.
    """
    return UserResponse(
        id=str(current_user.id),
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role,
        department=current_user.department,
        is_admin=current_user.is_admin,
        preferred_learning_style=current_user.preferred_learning_style.value if hasattr(current_user.preferred_learning_style, 'value') else str(current_user.preferred_learning_style),
        current_skills=current_user.current_skills or [],
        target_skills=current_user.target_skills or []
    )


@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    """
    Logout current user.
    Note: In a stateless JWT system, logout is handled client-side by discarding the token.
    For enhanced security, implement a token blacklist using Redis.
    """
    return {"message": "Successfully logged out"}
