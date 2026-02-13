from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.models import User, UserInteraction, Asset, InteractionStatus
from app.services.adaptive_engine import AdaptiveEngine
from datetime import datetime

router = APIRouter()

@router.get("/learning/{user_id}/next", response_model=Asset)
def get_next_recommendation(user_id: str, session: Session = Depends(get_session)):
    engine = AdaptiveEngine(session)
    # Refactor to use the new recommendation logic for consistency
    assets = engine.get_recommendations(user_id, limit=1)
    if not assets:
        raise HTTPException(status_code=404, detail="No more recommendations available or user not found.")
    return assets[0]

@router.get("/learning/{user_id}/recommendations", response_model=List[Asset])
def get_user_recommendations(user_id: str, session: Session = Depends(get_session)):
    """
    Get top N recommended assets for data-driven choice.
    """
    engine = AdaptiveEngine(session)
    assets = engine.get_recommendations(user_id, limit=3)
    return assets

from pydantic import BaseModel

class InteractionResponse(BaseModel):
    interaction: UserInteraction
    message: str
    next_recommendation: Optional[Asset] = None
    cheatsheet: Optional[str] = None
    remedial: bool = False

@router.post("/learning/interact", response_model=InteractionResponse)
def record_interaction(interaction: UserInteraction, session: Session = Depends(get_session)):
    # 1. Save interaction
    session.add(interaction)
    session.commit()
    session.refresh(interaction)
    
    response = InteractionResponse(
        interaction=interaction,
        message="Progress recorded."
    )

    # 2. Update Skill Mastery & Determine Next Step
    if interaction.status == InteractionStatus.COMPLETED and interaction.score is not None:
        asset = session.get(Asset, interaction.asset_id)
        
        # A. High Score Logic (Fast-Track)
        if interaction.score >= 80:
            response.message = f"🎉 Excellent! You scored {interaction.score}%. We've updated your adaptive profile."
            
            # Update Skill Mastery (Existing Logic)
            if asset and asset.skill_tag:
                from app.models.models import SkillMastery
                mastery = session.exec(
                    select(SkillMastery)
                    .where(SkillMastery.user_id == interaction.user_id)
                    .where(SkillMastery.skill_name == asset.skill_tag)
                ).first()

                if not mastery:
                    mastery = SkillMastery(
                        user_id=interaction.user_id,
                        skill_name=asset.skill_tag,
                        proficiency=0.0
                    )
                
                # Boost proficiency
                if mastery.proficiency < 100:
                    difficulty_boost = asset.difficulty_level * 2
                    score_multiplier = interaction.score / 100.0
                    increment = difficulty_boost * score_multiplier
                    mastery.proficiency = min(100.0, mastery.proficiency + increment)
                    mastery.last_updated = datetime.utcnow()
                    session.add(mastery)
                    session.commit()

            # Get Immediate Next Recommendation (Harder)
            engine = AdaptiveEngine(session)
            next_asset = engine.recommend_next_asset(interaction.user_id)
            if next_asset:
                response.next_recommendation = next_asset
                response.message += " Ready for the next challenge?"

        # B. Low Score Logic (Remedial)
        else:
            response.message = f"You scored {interaction.score}%. Let's review the key concepts before moving on."
            response.remedial = True
            if asset and asset.cheatsheet:
                response.cheatsheet = asset.cheatsheet

    return response

@router.get("/learning/dashboard/{user_id}")
def get_dashboard_stats(user_id: str, session: Session = Depends(get_session)):
    # Simple stats for the dashboard
    from app.models.models import User, UserInteraction
    from sqlmodel import select, func

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    interactions = session.exec(select(UserInteraction).where(UserInteraction.user_id == user_id)).all()
    completed = [i for i in interactions if i.status == InteractionStatus.COMPLETED]
    
    avg_score = 0
    if completed:
        scores = [i.score for i in completed if i.score is not None]
        if scores:
            avg_score = sum(scores) / len(scores)

    return {
        "user_name": user.full_name,
        "completed_modules": len(completed),
        "average_score": round(avg_score, 1),
        "current_level": "Intermediate", # Placeholder logic
        "learning_style": user.preferred_learning_style
    }
