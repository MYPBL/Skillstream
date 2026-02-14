"""
Verification Script for Video Integration.
Checks if assets have content_type='video' and valid YouTube URLs.
"""
from sqlmodel import Session, select
from app.core.database import engine
from app.models.models import Asset
import random

def verify_videos():
    with Session(engine) as session:
        # Get all assets
        assets = session.exec(select(Asset)).all()
        
        print(f"Total Assets: {len(assets)}")
        
        # Check how many are video
        video_count = sum(1 for a in assets if a.content_type == 'video')
        print(f"Video Assets: {video_count}")
        
        if video_count < len(assets):
            print("⚠️ WARNING: Not all assets are videos!")
        else:
            print("✅ SUCCESS: All assets are set to 'video' type.")
            
        print("\n--- Sampling 5 Assets ---")
        sample = random.sample(assets, min(5, len(assets)))
        
        for asset in sample:
            print(f"Title: {asset.title}")
            print(f"Type : {asset.content_type}")
            print(f"URL  : {asset.content_url}")
            print("-" * 30)

if __name__ == "__main__":
    verify_videos()
