"""
Video Content Populator.
Updates ALL assets to have video content (YouTube Embeds) based on their title/topic.
REQ: generic "add video to every module"
"""
from sqlmodel import Session, select
from app.core.database import engine
from app.models.models import Asset

# YouTube Embed URLs
VIDEOS = {
    "python": "https://www.youtube.com/embed/_uQrJ0TkZlc",   # Programming with Mosh: Python
    "react": "https://www.youtube.com/embed/SqcY0GlETPk",    # Programming with Mosh: React
    "javascript": "https://www.youtube.com/embed/W6NZfCO5SIk", # Programming with Mosh: JS
    "js": "https://www.youtube.com/embed/W6NZfCO5SIk",
    "html": "https://www.youtube.com/embed/qz0aGYrrlhU",     # Mosh HTML
    "css": "https://www.youtube.com/embed/qz0aGYrrlhU",      # Mosh HTML/CSS
    "java": "https://www.youtube.com/embed/eIrMbAQSU34",     # Mosh Java
    "default": "https://www.youtube.com/embed/k9WqpQp8LLU"   # Generic Coding
}

def add_video_content():
    with Session(engine) as session:
        assets = session.exec(select(Asset)).all()
        print(f"Found {len(assets)} assets. Updating with video content...\n")
        
        updated_count = 0
        
        for asset in assets:
            title_lower = asset.title.lower()
            
            # Default to generic
            video_url = VIDEOS["default"]
            
            # match topic
            for key, url in VIDEOS.items():
                if key in title_lower:
                    video_url = url
                    break
            
            # Update Asset
            asset.content_type = "video"
            asset.content_url = video_url
            
            session.add(asset)
            updated_count += 1
            print(f"🎥 {asset.title[:30]}... -> {video_url[-11:]}")
            
        session.commit()
        print(f"\n🎉 Successfully updated {updated_count} assets with video modules!")

if __name__ == "__main__":
    add_video_content()
