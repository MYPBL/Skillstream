from sqlmodel import Session, select
from app.core.database import engine, create_db_and_tables
from app.models.models import User, Asset, AssetVersion, LearningStyle
from app.core.security import get_password_hash

def create_seed_data():
    create_db_and_tables()
    with Session(engine) as session:
        # check if data exists
        if session.exec(select(User)).first():
            print("Data already exists. Skipping seed.")
            return

        # --- Users ---
        # Default password for all demo users: "password123"
        default_password = get_password_hash("password123")
        
        user_struggling = User(
            email="newbie@example.com", 
            full_name="Newbie Ned",
            hashed_password=default_password,
            role="Junior Developer",
            department="Engineering",
            employee_id="EMP001",
            current_skills=["HTML", "CSS"],
            target_skills=["Python", "JavaScript", "React"],
            preferred_learning_style=LearningStyle.VIDEO,
            learning_pace="slow",
            is_active=True,
            is_admin=False
        )
        user_fast = User(
            email="fast@example.com", 
            full_name="Fast Fiona",
            hashed_password=default_password,
            role="Senior Developer",
            department="Engineering",
            employee_id="EMP002",
            current_skills=["Python", "JavaScript", "SQL"],
            target_skills=["Kubernetes", "AWS", "Machine Learning"],
            preferred_learning_style=LearningStyle.TEXT,
            learning_pace="fast",
            is_active=True,
            is_admin=False
        )
        
        # Admin user
        admin_user = User(
            email="admin@example.com",
            full_name="Admin User",
            hashed_password=default_password,
            role="Platform Administrator",
            department="IT",
            employee_id="ADMIN001",
            current_skills=["System Administration", "DevOps"],
            target_skills=[],
            preferred_learning_style=LearningStyle.TEXT,
            learning_pace="medium",
            is_active=True,
            is_admin=True
        )
        
        session.add(user_struggling)
        session.add(user_fast)
        session.add(admin_user)
        session.flush() # Get IDs

        # --- Assets ---
        # Create assets with versions
        assets_data = [
            {
                "title": "Intro to Python",
                "description": "Video tutorial on variables and loops.",
                "content_url": "https://www.youtube.com/embed/_uQrJ0TkZlc",
                "content_type": "video",
                "skill_tag": "Python",
                "difficulty_level": 1,
                "estimated_duration_minutes": 10
            },
            {
                "title": "Python Syntax Guide",
                "description": "Text-based guide on syntax.",
                "content_url": "https://docs.python.org/3/tutorial/introduction.html",
                "content_type": "html5",
                "skill_tag": "Python",
                "difficulty_level": 1,
                "estimated_duration_minutes": 5
            },
            {
                "title": "Python Lists & Dicts",
                "description": "Deep dive into data structures.",
                "content_url": "https://realpython.com/python-lists-tuples/",
                "content_type": "html5",
                "skill_tag": "Python",
                "difficulty_level": 2,
                "estimated_duration_minutes": 15
            },
            {
                "title": "Interactive Python Shell",
                "description": "Practice basic commands.",
                "content_url": "https://www.python.org/shell/",
                "content_type": "scorm",
                "skill_tag": "Python",
                "difficulty_level": 2,
                "estimated_duration_minutes": 10
            },
            {
                "title": "Decorators Explained",
                "description": "Advanced functional programming.",
                "content_url": "https://www.youtube.com/embed/FsAPt_9Bf3U",
                "content_type": "video",
                "skill_tag": "Python",
                "difficulty_level": 3,
                "estimated_duration_minutes": 20
            }
        ]
        
        for data in assets_data:
            # Create Asset
            asset = Asset(
                title=data["title"],
                description=data["description"],
                content_type=data["content_type"],
                content_url=data["content_url"],
                skill_tag=data["skill_tag"],
                difficulty_level=data["difficulty_level"],
                estimated_duration_minutes=data["estimated_duration_minutes"],
                created_by=str(admin_user.id),
                current_version=1
            )
            session.add(asset)
            session.flush()
            
            # Create Version
            version = AssetVersion(
                asset_id=asset.id,
                version=1,
                content_url=data["content_url"],
                content_type=data["content_type"],
                created_by=str(admin_user.id)
            )
            session.add(version)
        
        session.commit()
        print("Seed data created successfully with versioned assets!")

if __name__ == "__main__":
    create_seed_data()
