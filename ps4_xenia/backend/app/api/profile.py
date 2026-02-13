"""
User Profile Management API endpoints.
Handles profile retrieval, updates, and learning history.
"""
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from pydantic import BaseModel
from app.core.database import get_session
from app.core.security import get_current_user, get_current_admin_user
from app.models.models import User, UserInteraction, LearningStyle
from app.core.cache import cache_get, cache_set, cache_delete

router = APIRouter()


# --- Request/Response Models ---

class ProfileUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    department: Optional[str] = None
    role: Optional[str] = None
    current_skills: Optional[List[str]] = None
    target_skills: Optional[List[str]] = None
    preferred_learning_style: Optional[str] = None
    learning_pace: Optional[str] = None


class ProfileResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    department: Optional[str]
    employee_id: Optional[str]
    current_skills: List[str]
    target_skills: List[str]
    preferred_learning_style: str
    learning_pace: str
    is_admin: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]


class LearningHistoryItem(BaseModel):
    asset_id: str
    asset_title: str
    status: str
    score: Optional[float]
    time_spent_seconds: int
    attempts: int
    timestamp: datetime


# --- Endpoints ---

@router.get("/profile", response_model=ProfileResponse)
async def get_my_profile(current_user: User = Depends(get_current_user)):
    """
    Get current user's profile.
    
    WHEN an Employee requests their profile,
    THE Backend_Service SHALL retrieve it within 100ms.
    """
    return ProfileResponse(
        id=str(current_user.id),
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role,
        department=current_user.department,
        employee_id=current_user.employee_id,
        current_skills=current_user.current_skills or [],
        target_skills=current_user.target_skills or [],
        preferred_learning_style=current_user.preferred_learning_style.value if hasattr(current_user.preferred_learning_style, 'value') else str(current_user.preferred_learning_style),
        learning_pace=current_user.learning_pace,
        is_admin=current_user.is_admin,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
        last_login=current_user.last_login
    )


@router.get("/profile/{user_id}", response_model=ProfileResponse)
async def get_user_profile(
    user_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get any user's profile (admin only or own profile).
    
    WHEN an Employee requests their profile,
    THE Backend_Service SHALL retrieve it within 100ms.
    
    Uses Redis caching for fast retrieval.
    """
    # Users can view their own profile, admins can view any profile
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this profile"
        )
    
    # Try to get from cache first
    cache_key = f"profile:{user_id}"
    cached_profile = await cache_get(cache_key)
    if cached_profile:
        return ProfileResponse(**cached_profile)
    
    # Cache miss - fetch from database
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    profile_data = {
        "id": str(user.id),
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "department": user.department,
        "employee_id": user.employee_id,
        "current_skills": user.current_skills or [],
        "target_skills": user.target_skills or [],
        "preferred_learning_style": user.preferred_learning_style.value if hasattr(user.preferred_learning_style, 'value') else str(user.preferred_learning_style),
        "learning_pace": user.learning_pace,
        "is_admin": user.is_admin,
        "created_at": user.created_at.isoformat(),
        "updated_at": user.updated_at.isoformat(),
        "last_login": user.last_login.isoformat() if user.last_login else None
    }
    
    # Cache for 5 minutes
    await cache_set(cache_key, profile_data, ttl=300)
    
    return ProfileResponse(**profile_data)


@router.patch("/profile", response_model=ProfileResponse)
async def update_my_profile(
    updates: ProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update current user's profile.
    
    WHEN an Employee updates their profile,
    THE Backend_Service SHALL update the profile and notify the Adaptive_Engine.
    
    Invalidates cache after update.
    """
    # Track if skills changed (for Adaptive Engine notification)
    skills_changed = (
        (updates.current_skills is not None and updates.current_skills != current_user.current_skills) or
        (updates.target_skills is not None and updates.target_skills != current_user.target_skills)
    )
    
    # Update allowed fields
    if updates.full_name is not None:
        current_user.full_name = updates.full_name
    if updates.department is not None:
        current_user.department = updates.department
    if updates.role is not None:
        current_user.role = updates.role
    if updates.current_skills is not None:
        current_user.current_skills = updates.current_skills
    if updates.target_skills is not None:
        current_user.target_skills = updates.target_skills
    if updates.preferred_learning_style is not None:
        try:
            current_user.preferred_learning_style = LearningStyle(updates.preferred_learning_style)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid learning style. Must be one of: {[ls.value for ls in LearningStyle]}"
            )
    if updates.learning_pace is not None:
        if updates.learning_pace not in ["slow", "medium", "fast"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Learning pace must be 'slow', 'medium', or 'fast'"
            )
        current_user.learning_pace = updates.learning_pace
    
    # Update timestamp
    current_user.updated_at = datetime.utcnow()
    
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    
    # Invalidate cache
    await cache_delete(f"profile:{current_user.id}")
    
    # TODO: Notify Adaptive Engine of profile update if skills changed
    # This will trigger path recalculation
    # if skills_changed:
    #     await notify_adaptive_engine(current_user.id, updates)
    
    return ProfileResponse(
        id=str(current_user.id),
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role,
        department=current_user.department,
        employee_id=current_user.employee_id,
        current_skills=current_user.current_skills or [],
        target_skills=current_user.target_skills or [],
        preferred_learning_style=current_user.preferred_learning_style.value if hasattr(current_user.preferred_learning_style, 'value') else str(current_user.preferred_learning_style),
        learning_pace=current_user.learning_pace,
        is_admin=current_user.is_admin,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
        last_login=current_user.last_login
    )


@router.get("/profile/history", response_model=List[LearningHistoryItem])
async def get_my_learning_history(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    limit: int = 50
):
    """
    Get current user's learning history.
    
    WHEN an Employee requests their learning history,
    THE Backend_Service SHALL return all completed interactions.
    """
    from app.models.models import Asset
    
    # Get user's interactions
    interactions = session.exec(
        select(UserInteraction)
        .where(UserInteraction.user_id == current_user.id)
        .order_by(UserInteraction.timestamp.desc())
        .limit(limit)
    ).all()
    
    # Build response with asset details
    history = []
    for interaction in interactions:
        asset = session.get(Asset, interaction.asset_id)
        if asset:
            history.append(LearningHistoryItem(
                asset_id=str(interaction.asset_id),
                asset_title=asset.title,
                status=interaction.status.value if hasattr(interaction.status, 'value') else str(interaction.status),
                score=interaction.score,
                time_spent_seconds=interaction.time_spent_seconds,
                attempts=interaction.attempts,
                timestamp=interaction.timestamp
            ))
    
    return history


@router.get("/profile/{user_id}/history", response_model=List[LearningHistoryItem])
async def get_user_learning_history(
    user_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    limit: int = 50
):
    """
    Get any user's learning history (admin only or own history).
    """
    # Users can view their own history, admins can view any history
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this learning history"
        )
    
    from app.models.models import Asset
    
    # Get user's interactions
    interactions = session.exec(
        select(UserInteraction)
        .where(UserInteraction.user_id == user_id)
        .order_by(UserInteraction.timestamp.desc())
        .limit(limit)
    ).all()
    
    # Build response with asset details
    history = []
    for interaction in interactions:
        asset = session.get(Asset, interaction.asset_id)
        if asset:
            history.append(LearningHistoryItem(
                asset_id=str(interaction.asset_id),
                asset_title=asset.title,
                status=interaction.status.value if hasattr(interaction.status, 'value') else str(interaction.status),
                score=interaction.score,
                time_spent_seconds=interaction.time_spent_seconds,
                attempts=interaction.attempts,
                timestamp=interaction.timestamp
            ))
    
    return history


@router.get("/profile/skills", response_model=dict)
async def get_my_skills(current_user: User = Depends(get_current_user)):
    """
    Get current user's skills summary.
    """
    return {
        "current_skills": current_user.current_skills or [],
        "target_skills": current_user.target_skills or [],
        "skill_gaps": list(set(current_user.target_skills or []) - set(current_user.current_skills or []))
    }
