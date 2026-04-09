import sys
sys.path.insert(0, '/d:/COMPETITIVE_EXAM/backend')

from app.database import SessionLocal, engine
from app import models, crud
from app.schemas import UserCreate

# Create tables
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # Check if test user exists
    existing_user = crud.get_user_by_email(db, "test@example.com")
    if existing_user:
        print(f"✓ User already exists: {existing_user.email}")
    else:
        # Create test user
        user_data = UserCreate(
            name="Test User",
            email="test@example.com",
            password="password"
        )
        new_user = crud.create_user(db, user_data)
        print(f"✓ User created: {new_user.email}")
        print(f"  ID: {new_user.id}")
        print(f"  Name: {new_user.name}")
finally:
    db.close()

print("\n✓ Done!")
