from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import create_db_and_tables
from app.api import admin, learning, auth, profile

app = FastAPI(title="Dynamic Professional Development Platform")
# Trigger Reload for Phase 8 Config

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:8001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Dynamic PDP API"}

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(profile.router, prefix="/api/v1", tags=["profile"])
app.include_router(admin.router, prefix="/api/v1", tags=["admin"])
app.include_router(learning.router, prefix="/api/v1", tags=["learning"])

from app.api import analytics, notifications
app.include_router(analytics.router, prefix="/api/v1", tags=["analytics"])
app.include_router(notifications.router, prefix="/api/v1", tags=["notifications"])

# Late import to avoid circular dependency if needed, or better organize admins
from app.api import admin_assets, assets
app.include_router(admin_assets.router, prefix="/api/v1/admin", tags=["admin-assets"])
app.include_router(assets.router, prefix="/api/v1", tags=["library"])
