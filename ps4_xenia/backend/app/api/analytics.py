from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, func
from datetime import datetime, timedelta
from app.core.database import get_session
from app.models.models import User, UserInteraction, SkillMastery, InteractionStatus

router = APIRouter()

@router.get("/analytics/{user_id}/overview")
def get_analytics_overview(user_id: str, session: Session = Depends(get_session)):
    """
    Get high-level performance metrics: Total Time, Completed Modules, Current Streak (Mock).
    """
    # Total Time Spent
    total_time_seconds = session.exec(
        select(func.sum(UserInteraction.time_spent_seconds))
        .where(UserInteraction.user_id == user_id)
    ).one() or 0
    
    # Completed Modules
    completed_count = session.exec(
        select(func.count(UserInteraction.id))
        .where(UserInteraction.user_id == user_id)
        .where(UserInteraction.status == InteractionStatus.COMPLETED)
    ).one() or 0

    # Calculate "Streak" (days with at least one interaction in last 7 days)
    # Simplified Logic: Check distinct dates in last 7 days
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_interactions = session.exec(
        select(UserInteraction.timestamp)
        .where(UserInteraction.user_id == user_id)
        .where(UserInteraction.timestamp >= seven_days_ago)
    ).all()
    
    unique_days = {dt.date() for dt in recent_interactions}
    current_streak = len(unique_days) # Placeholder logic for streak

    return {
        "total_learning_hours": round(total_time_seconds / 3600, 1),
        "modules_completed": completed_count,
        "current_streak_days": current_streak,
        "efficiency_score": 92 # Placeholder or calculate based on time vs estimated
    }

@router.get("/analytics/{user_id}/skills")
def get_skill_radar_data(user_id: str, session: Session = Depends(get_session)):
    """
    Get skill mastery data for Radar Chart.
    """
    skills = session.exec(
        select(SkillMastery).where(SkillMastery.user_id == user_id)
    ).all()

    if not skills:
        # Return default structure if no data yet
        return [
            {"subject": "Python", "A": 0, "fullMark": 100},
            {"subject": "React", "A": 0, "fullMark": 100},
            {"subject": "System Design", "A": 0, "fullMark": 100},
            {"subject": "DevOps", "A": 0, "fullMark": 100},
            {"subject": "Data Science", "A": 0, "fullMark": 100},
             {"subject": "Security", "A": 0, "fullMark": 100},
        ]
    
    return [
        {"subject": s.skill_name, "A": int(s.proficiency), "fullMark": 100}
        for s in skills
    ]

@router.get("/analytics/{user_id}/activity")
def get_activity_data(user_id: str, session: Session = Depends(get_session)):
    """
    Get last 7 days activity (minutes spent) for Bar Chart.
    """
    today = datetime.utcnow().date()
    data = []
    
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        day_start = datetime.combine(day, datetime.min.time())
        day_end = datetime.combine(day, datetime.max.time())
        
        minutes = session.exec(
            select(func.sum(UserInteraction.time_spent_seconds))
            .where(UserInteraction.user_id == user_id)
            .where(UserInteraction.timestamp >= day_start)
            .where(UserInteraction.timestamp <= day_end)
        ).one() or 0
        
        data.append({
            "name": day.strftime("%a"), # Mon, Tue...
            "minutes": round(minutes / 60)
        })
        
    return data
