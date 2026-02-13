from app.main import app

print("=== Registered Routes ===")
for route in app.routes:
    print(f"{route.methods if hasattr(route, 'methods') else 'N/A'} {route.path}")
