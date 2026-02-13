from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship, Column, JSON
from enum import Enum

class UserRole(str, Enum):
    EMPLOYEE = "employee"
    ADMIN = "admin"

class LearningStyle(str, Enum):
    VIDEO = "video"
    TEXT = "text"
    INTERACTIVE = "interactive"

class AssetType(str, Enum):
    VIDEO = "video"
    DOCUMENTATION = "documentation"
    SANDBOX = "sandbox"

class InteractionStatus(str, Enum):
    STARTED = "started"
    COMPLETED = "completed"
    FAILED = "failed"

class PathStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

# --- Models ---

class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, index=True)
    email: str = Field(unique=True, index=True)
    full_name: str
    
    # Authentication fields
    hashed_password: str
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False)
    last_login: Optional[datetime] = None
    
    # Enterprise profile fields
    role: str = Field(default="Employee")  # Job role (e.g., "Software Engineer")
    department: Optional[str] = None  # e.g., "Engineering", "Sales"
    employee_id: Optional[str] = Field(default=None, unique=True, index=True)
    
    # Skills tracking
    current_skills: List[str] = Field(default=[], sa_column=Column(JSON))
    target_skills: List[str] = Field(default=[], sa_column=Column(JSON))
    
    # Learning preferences
    preferred_learning_style: LearningStyle = Field(default=LearningStyle.VIDEO)
    learning_pace: str = Field(default="medium")  # slow, medium, fast
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    interactions: List["UserInteraction"] = Relationship(back_populates="user")
    learning_paths: List["LearningPath"] = Relationship(back_populates="user")
    skill_mastery: List["SkillMastery"] = Relationship(back_populates="user")

class SkillMastery(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, index=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    skill_name: str
    proficiency: float = Field(default=0.0) # 0.0 to 100.0
    last_updated: datetime = Field(default_factory=datetime.utcnow)

    user: User = Relationship(back_populates="skill_mastery")

class Asset(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, index=True)
    title: str
    description: str
    
    # Content fields
    content_type: str = Field(default="video") # video, pdf, scorm, html5
    content_url: str
    current_version: int = Field(default=1)
    file_size_bytes: Optional[int] = None
    
    # Metadata
    skill_tag: str
    difficulty_level: int = Field(ge=1, le=5)  # 1-5
    estimated_duration_minutes: int
    
    # Phase 8: Interactive Quiz Support
    quiz_data: Optional[List[dict]] = Field(default=None, sa_column=Column(JSON))
    cheatsheet: Optional[str] = None # Markdown summary for remedial review
    
    # Status
    is_active: bool = Field(default=True)
    is_archived: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str = Field(foreign_key="user.id") # Admin User ID

    interactions: List["UserInteraction"] = Relationship(back_populates="asset")
    versions: List["AssetVersion"] = Relationship(back_populates="asset")

class AssetVersion(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, index=True)
    asset_id: str = Field(foreign_key="asset.id")
    version: int
    content_url: str
    content_type: str
    file_size_bytes: Optional[int]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str = Field(foreign_key="user.id")
    
    asset: Asset = Relationship(back_populates="versions")

class LearningPath(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, index=True)
    user_id: str = Field(foreign_key="user.id")
    name: str
    status: PathStatus = Field(default=PathStatus.IN_PROGRESS)
    
    user: User = Relationship(back_populates="learning_paths")

class UserInteraction(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, index=True)
    user_id: str = Field(foreign_key="user.id")
    asset_id: str = Field(foreign_key="asset.id")
    status: InteractionStatus = Field(default=InteractionStatus.STARTED)
    score: Optional[float] = None # 0.0 to 1.0 (or 100.0)
    time_spent_seconds: int = Field(default=0)
    attempts: int = Field(default=1)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    user: User = Relationship(back_populates="interactions")
    asset: Asset = Relationship(back_populates="interactions")

class Notification(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, index=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    message: str
    type: str = Field(default="info") # info, success, warning
    is_read: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
