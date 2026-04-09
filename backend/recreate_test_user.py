from app.database import SessionLocal, engine
from app import models, crud
from app.schemas import UserCreate
from app.auth import hash_password

# Create tables
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # Delete existing test user
    existing = crud.get_user_by_email(db, 'test@example.com')
    if existing:
        db.delete(existing)
        db.commit()
        print('✓ Deleted old test user')
    
    # Create fresh test user
    password = 'password'
    hashed = hash_password(password)
    print(f'Creating user with password: "{password}"')
    print(f'Hash will be: {hashed}')
    
    user_data = UserCreate(
        name='Test User',
        email='test@example.com',
        password=password
    )
    new_user = crud.create_user(db, user_data)
    print(f'✓ User created: {new_user.email}')
    print(f'  Password hash: {new_user.password_hash}')
    
    # Now test verification
    from app.auth import verify_password
    result = verify_password(password, new_user.password_hash)
    print(f'✓ Verification test: {result}')
    
finally:
    db.close()

print('\n✓ Done!')
