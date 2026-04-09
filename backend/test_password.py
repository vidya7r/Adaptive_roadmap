from app.database import SessionLocal
from app import crud
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

db = SessionLocal()
user = crud.get_user_by_email(db, 'test@example.com')
db.close()

if user:
    print(f'User: {user.email}')
    print(f'Hash: {user.password_hash}')
    print(f'Testing with password: "password"')
    try:
        result = pwd_context.verify('password', user.password_hash)
        print(f'✓ Verification result: {result}')
    except Exception as e:
        print(f'✗ ERROR: {type(e).__name__}: {e}')
else:
    print('User not found')
