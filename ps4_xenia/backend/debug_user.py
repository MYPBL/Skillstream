"""
Direct test of get_current_user to see the actual error.
"""
from app.core.security import create_access_token, decode_token
from app.core.database import engine
from sqlmodel import Session, select
from app.models.models import User

# Create a token
token = create_access_token(data={"sub": "7661345d-220e-43a2-a896-967a1ef9ce53"})
print(f"Token created: {token[:50]}...")

# Decode it
payload = decode_token(token)
print(f"Payload: {payload}")

# Try to get user
with Session(engine) as session:
    user_id = payload.get("sub")
    print(f"User ID from token: {user_id}")
    
    user = session.get(User, user_id)
    print(f"User found: {user}")
    
    if user:
        print(f"User details:")
        print(f"  - ID: {user.id}")
        print(f"  - Email: {user.email}")
        print(f"  - Full Name: {user.full_name}")
        print(f"  - Role: {user.role}")
        print(f"  - Department: {user.department}")
        print(f"  - Is Admin: {user.is_admin}")
        print(f"  - Preferred Learning Style: {user.preferred_learning_style}")
        print(f"  - Type: {type(user.preferred_learning_style)}")
        print(f"  - Has value attr: {hasattr(user.preferred_learning_style, 'value')}")
        if hasattr(user.preferred_learning_style, 'value'):
            print(f"  - Value: {user.preferred_learning_style.value}")
        print(f"  - Current Skills: {user.current_skills}")
        print(f"  - Target Skills: {user.target_skills}")
