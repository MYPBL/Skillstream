"""
Verification Script for Phase 4: Adaptive Algorithm
Tests the scoring logic: Skill Matching, Difficulty, etc.
"""
from sqlmodel import Session, create_engine, SQLModel, select 
from app.models.models import User, Asset, UserInteraction, AssetType, LearningStyle
from app.services.adaptive_engine import AdaptiveEngine
from app.core.config import settings
from datetime import datetime

# Use in-memory DB for pure logic test or connect to local dev DB
# Let's use local dev DB to use existing schema but we'll create temporary test data
# Actually, let's use a separate in-memory DB to avoid polluting the main DB and ensure clean state
sqlite_url = "sqlite://" # In-memory
engine = create_engine(sqlite_url)
SQLModel.metadata.create_all(engine)

def verify_algorithm():
    print("🧪 Starting Algorithm Verification...")
    
    with Session(engine) as session:
        # 1. Setup User
        user = User(
            email="algotester@example.com", 
            hashed_password="pw", 
            full_name="Algo Tester",
            target_skills=["FastAPI", "React"], # WANTS these
            current_skills=["Python"],          # HAS these
            preferred_learning_style="video",
            learning_pace="medium",
            role="Frontend Developer"
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        print(f"   Created User: {user.email} (Target: {user.target_skills})")

        # 2. Setup Assets
        # Asset A: Perfect Match (Skill=FastAPI, Diff=1, Type=video)
        # Score Expectation: 
        #   Diff(1 vs 1) = +30
        #   Skill(FastAPI) = +40
        #   Type(video) = +10
        #   TOTAL = ~80
        asset_a = Asset(
            title="FastAPI for Beginners",
            description="Perfect match",
            content_type="video",
            content_url="http://x",
            skill_tag="FastAPI",
            difficulty_level=1,
            estimated_duration_minutes=10,
            created_by=user.id
        )
        
        # Asset B: Good Skill, Wrong Type (Skill=React, Diff=1, Type=pdf)
        # Score Expectation:
        #   Diff = +30
        #   Skill(React) = +40
        #   Type(pdf vs video) = 0
        #   TOTAL = ~70
        asset_b = Asset(
            title="React Docs",
            description="Good skill, wrong format",
            content_type="pdf",
            content_url="http://y",
            skill_tag="React",
            difficulty_level=1,
            estimated_duration_minutes=20,
            created_by=user.id
        )
        
        # Asset C: Irrelevant Skill (Skill=Java, Diff=1)
        # Score Expectation:
        #   Diff = +30
        #   Skill(Java) = 0
        #   TOTAL = ~30
        asset_c = Asset(
            title="Java Basics",
            description="Irrelevant",
            content_type="video",
            content_url="http://z",
            skill_tag="Java",
            difficulty_level=1,
            estimated_duration_minutes=30,
            created_by=user.id
        )

        session.add(asset_a)
        session.add(asset_b)
        session.add(asset_c)
        session.commit()
        
        # 3. Run Algorithm
        adaptive = AdaptiveEngine(session)
        recs = adaptive.get_recommendations(user.id, limit=3)
        
        # 4. Assertions
        print(f"   Recommendations: {[a.title for a in recs]}")
        
        if not recs:
            print("❌ FAIL: No recommendations returned")
            exit(1)
            
        if recs[0].skill_tag not in ["FastAPI", "React"]:
             print(f"❌ FAIL: Top result {recs[0].title} is not a target skill match")
             exit(1)
             
        # Check Ranking: A should be > C
        # Find index
        idx_a = -1
        idx_c = -1
        for i, r in enumerate(recs):
            if r.title == asset_a.title: idx_a = i
            if r.title == asset_c.title: idx_c = i
            
        if idx_a < idx_c: # Lower index = higher rank
             print("✅ PASS: Relevant asset matches higher than irrelevant one")
        else:
             print("❌ FAIL: Irrelevant asset ranked higher or equal")
             exit(1)

        print("✅ ALGORITHM VERIFICATION SUCCESSFUL")

if __name__ == "__main__":
    verify_algorithm()
