"""
Admin Asset Management API endpoints.
Handles asset creation, updates (versioning), and archival.
"""
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from pydantic import BaseModel
from app.core.database import get_session
from app.core.security import get_current_admin_user
from app.models.models import User, Asset, AssetVersion

router = APIRouter()


# --- Request/Response Models ---

class AssetCreateRequest(BaseModel):
    title: str
    description: str
    content_type: str  # video, pdf, scorm, html5
    content_url: str
    file_size_bytes: Optional[int] = None
    skill_tag: str
    difficulty_level: int  # 1-5
    estimated_duration_minutes: int


class AssetUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content_url: Optional[str] = None  # If provided, creates new version
    file_size_bytes: Optional[int] = None
    skill_tag: Optional[str] = None
    difficulty_level: Optional[int] = None
    estimated_duration_minutes: Optional[int] = None
    is_active: Optional[bool] = None


class AssetResponse(BaseModel):
    id: str
    title: str
    description: str
    content_type: str
    content_url: str
    current_version: int
    skill_tag: str
    difficulty_level: int
    estimated_duration_minutes: int
    is_active: bool
    is_archived: bool
    created_at: datetime
    updated_at: datetime
    created_by: str


class AssetVersionResponse(BaseModel):
    id: str
    version: int
    content_url: str
    content_type: str
    created_at: datetime
    created_by: str


# --- Admin Endpoints ---

@router.post("/assets", response_model=AssetResponse)
async def create_asset(
    asset_data: AssetCreateRequest,
    current_user: User = Depends(get_current_admin_user),
    session: Session = Depends(get_session)
):
    """
    Create a new learning asset.
    Admin only.
    """
    # Create asset
    new_asset = Asset(
        title=asset_data.title,
        description=asset_data.description,
        content_type=asset_data.content_type,
        content_url=asset_data.content_url,
        file_size_bytes=asset_data.file_size_bytes,
        skill_tag=asset_data.skill_tag,
        difficulty_level=asset_data.difficulty_level,
        estimated_duration_minutes=asset_data.estimated_duration_minutes,
        created_by=str(current_user.id),
        current_version=1
    )
    
    session.add(new_asset)
    session.flush() # Get ID
    
    # Create initial version
    initial_version = AssetVersion(
        asset_id=new_asset.id,
        version=1,
        content_url=asset_data.content_url,
        content_type=asset_data.content_type,
        file_size_bytes=asset_data.file_size_bytes,
        created_by=str(current_user.id)
    )
    session.add(initial_version)
    
    session.commit()
    session.refresh(new_asset)
    
    return AssetResponse(
        id=str(new_asset.id),
        title=new_asset.title,
        description=new_asset.description,
        content_type=new_asset.content_type,
        content_url=new_asset.content_url,
        current_version=new_asset.current_version,
        skill_tag=new_asset.skill_tag,
        difficulty_level=new_asset.difficulty_level,
        estimated_duration_minutes=new_asset.estimated_duration_minutes,
        is_active=new_asset.is_active,
        is_archived=new_asset.is_archived,
        created_at=new_asset.created_at,
        updated_at=new_asset.updated_at,
        created_by=new_asset.created_by
    )


@router.get("/assets", response_model=List[AssetResponse])
async def list_assets(
    skip: int = 0,
    limit: int = 100,
    skill_tag: Optional[str] = None,
    content_type: Optional[str] = None,
    current_user: User = Depends(get_current_admin_user),
    session: Session = Depends(get_session)
):
    """
    List all assets (including archived).
    Admin only.
    """
    query = select(Asset)
    
    if skill_tag:
        query = query.where(Asset.skill_tag == skill_tag)
    if content_type:
        query = query.where(Asset.content_type == content_type)
        
    query = query.offset(skip).limit(limit)
    assets = session.exec(query).all()
    
    return assets


@router.patch("/assets/{asset_id}", response_model=AssetResponse)
async def update_asset(
    asset_id: str,
    updates: AssetUpdateRequest,
    current_user: User = Depends(get_current_admin_user),
    session: Session = Depends(get_session)
):
    """
    Update an asset.
    If content_url is provided, creates a new version.
    """
    asset = session.get(Asset, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
        
    # Check if we need to create a new version
    if updates.content_url and updates.content_url != asset.content_url:
        new_version_num = asset.current_version + 1
        
        new_version = AssetVersion(
            asset_id=asset.id,
            version=new_version_num,
            content_url=updates.content_url,
            content_type=asset.content_type, # Assume type doesn't change for now
            file_size_bytes=updates.file_size_bytes or asset.file_size_bytes,
            created_by=str(current_user.id)
        )
        session.add(new_version)
        
        asset.content_url = updates.content_url
        asset.current_version = new_version_num
        if updates.file_size_bytes:
            asset.file_size_bytes = updates.file_size_bytes
            
    # Update other fields
    if updates.title:
        asset.title = updates.title
    if updates.description:
        asset.description = updates.description
    if updates.skill_tag:
        asset.skill_tag = updates.skill_tag
    if updates.difficulty_level:
        asset.difficulty_level = updates.difficulty_level
    if updates.estimated_duration_minutes:
        asset.estimated_duration_minutes = updates.estimated_duration_minutes
    if updates.is_active is not None:
        asset.is_active = updates.is_active
        
    asset.updated_at = datetime.utcnow()
    session.add(asset)
    session.commit()
    session.refresh(asset)
    
    return AssetResponse(
        id=str(asset.id),
        title=asset.title,
        description=asset.description,
        content_type=asset.content_type,
        content_url=asset.content_url,
        current_version=asset.current_version,
        skill_tag=asset.skill_tag,
        difficulty_level=asset.difficulty_level,
        estimated_duration_minutes=asset.estimated_duration_minutes,
        is_active=asset.is_active,
        is_archived=asset.is_archived,
        created_at=asset.created_at,
        updated_at=asset.updated_at,
        created_by=asset.created_by
    )


@router.delete("/assets/{asset_id}")
async def archive_asset(
    asset_id: str,
    current_user: User = Depends(get_current_admin_user),
    session: Session = Depends(get_session)
):
    """
    Archive an asset (soft delete).
    """
    asset = session.get(Asset, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
        
    asset.is_archived = True
    asset.is_active = False
    asset.updated_at = datetime.utcnow()
    
    session.add(asset)
    session.commit()
    return {"message": "Asset archived successfully"}


@router.get("/assets/{asset_id}/versions", response_model=List[AssetVersionResponse])
async def get_asset_versions(
    asset_id: str,
    current_user: User = Depends(get_current_admin_user),
    session: Session = Depends(get_session)
):
    """
    Get version history for an asset.
    """
    versions = session.exec(
        select(AssetVersion)
        .where(AssetVersion.asset_id == asset_id)
        .order_by(AssetVersion.version.desc())
    ).all()
    
    return versions
