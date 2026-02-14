"""
Public Asset API for user consumption.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from pydantic import BaseModel
from app.core.database import get_session
from app.core.security import get_current_user
from app.models.models import User, Asset
from datetime import datetime

router = APIRouter()

class AssetPublicResponse(BaseModel):
    id: str
    title: str
    description: str
    content_type: str
    skill_tag: str
    difficulty_level: int
    estimated_duration_minutes: int
    created_at: datetime

import json
from app.core.database import get_session, redis_client

# ... (imports)

@router.get("/library", response_model=List[AssetPublicResponse])
async def get_asset_library(
    skill_tag: Optional[str] = None,
    content_type: Optional[str] = None,
    difficulty_level: Optional[int] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Browse learning assets library.
    Returns only active, non-archived assets.
    REQ-14: Content Delivery and Caching
    """
    # 1. Check Cache
    cache_key = f"assets_library:{skill_tag}:{content_type}:{difficulty_level}:{search}:{skip}:{limit}"
    
    if redis_client:
        try:
            cached_data = redis_client.get(cache_key)
            if cached_data:
                # Deserialize and return
                return [AssetPublicResponse(**item) for item in json.loads(cached_data)]
        except Exception as e:
            print(f"Cache Error: {e}")

    # 2. Query Database
    query = select(Asset).where(Asset.is_active == True, Asset.is_archived == False)
    
    if skill_tag:
        query = query.where(Asset.skill_tag == skill_tag)
    if content_type:
        query = query.where(Asset.content_type == content_type)
    if difficulty_level:
        query = query.where(Asset.difficulty_level == difficulty_level)
    if search:
        query = query.where(Asset.title.contains(search) | Asset.description.contains(search))
        
    query = query.order_by(Asset.created_at.desc()).offset(skip).limit(limit)
    assets = session.exec(query).all()
    
    response_data = [
        AssetPublicResponse(
            id=str(a.id),
            title=a.title,
            description=a.description,
            content_type=a.content_type,
            skill_tag=a.skill_tag,
            difficulty_level=a.difficulty_level,
            estimated_duration_minutes=a.estimated_duration_minutes,
            created_at=a.created_at
        ) for a in assets
    ]

    # 3. Set Cache (Expire in 1 hour)
    if redis_client:
        try:
            # Serialize with datetime handling (pydantic model dump handles standard types, but json.dumps needs default=str for datetime)
            serialized_data = json.dumps([r.model_dump(mode='json') for r in response_data])
            redis_client.setex(cache_key, 3600, serialized_data)
        except Exception as e:
            print(f"Cache Set Error: {e}")
            
    return response_data

@router.get("/library/{asset_id}", response_model=AssetPublicResponse)
async def get_asset_details(
    asset_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get details for a specific asset.
    """
    asset = session.get(Asset, asset_id)
    if not asset or asset.is_archived:
        raise HTTPException(status_code=404, detail="Asset not found")
        
    return AssetPublicResponse(
        id=str(asset.id),
        title=asset.title,
        description=asset.description,
        content_type=asset.content_type,
        skill_tag=asset.skill_tag,
        difficulty_level=asset.difficulty_level,
        estimated_duration_minutes=asset.estimated_duration_minutes,
        created_at=asset.created_at
    )

@router.get("/library/{asset_id}/content")
async def get_asset_content(
    asset_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get content URL for an asset.
    In a real app, this would generate a signed URL (e.g., S3/CloudFront).
    """
    asset = session.get(Asset, asset_id)
    if not asset or asset.is_archived:
        raise HTTPException(status_code=404, detail="Asset not found")
        
    # Mocking a signed URL generation
    return {
        "content_url": asset.content_url,
        "content_type": asset.content_type,
        "expires_in_seconds": 3600
    }
