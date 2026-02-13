from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.models import Notification

router = APIRouter()

@router.get("/notifications/{user_id}", response_model=List[Notification])
def get_user_notifications(user_id: str, session: Session = Depends(get_session)):
    """
    Get all notifications for a user, ordered by newest first.
    """
    notifications = session.exec(
        select(Notification)
        .where(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
    ).all()
    return notifications

@router.post("/notifications/{notification_id}/read")
def mark_notification_read(notification_id: str, session: Session = Depends(get_session)):
    """
    Mark a specific notification as read.
    """
    notification = session.get(Notification, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.is_read = True
    session.add(notification)
    session.commit()
    return {"status": "success"}
