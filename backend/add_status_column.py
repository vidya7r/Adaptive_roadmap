"""
Migration script to add 'status' column to user_subtopic_progress table
"""

from sqlalchemy import text
from app.database import SessionLocal, engine

def add_status_column():
    """Add status column if it doesn't exist"""
    db = SessionLocal()
    try:
        # Check if column exists
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'user_subtopic_progress' 
                AND column_name = 'status'
            """))
            
            column_exists = result.fetchone() is not None
            
            if not column_exists:
                print("✓ Adding 'status' column to user_subtopic_progress table...")
                conn.execute(text("""
                    ALTER TABLE user_subtopic_progress 
                    ADD COLUMN status VARCHAR(50) DEFAULT 'pending'
                """))
                conn.commit()
                print("✓ Column added successfully!")
            else:
                print("✓ 'status' column already exists!")
                
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        print("Note: If using SQLite, use this alternative:")
        print("""
        sqlite3 DATABASE_PATH << EOF
        ALTER TABLE user_subtopic_progress ADD COLUMN status VARCHAR(50) DEFAULT 'pending';
        EOF
        """)
    finally:
        db.close()

if __name__ == "__main__":
    add_status_column()
