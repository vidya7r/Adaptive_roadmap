"""
Simple SQLite migration to add 'status' column
Run this from the backend directory: python migrate_status.py
"""

import sqlite3
import os

def migrate():
    # Get database path
    db_path = os.path.join(os.path.dirname(__file__), 'app', 'database.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Try to add column
        try:
            cursor.execute("""
                ALTER TABLE user_subtopic_progress 
                ADD COLUMN status VARCHAR(50) DEFAULT 'pending'
            """)
            conn.commit()
            print("✓ Successfully added 'status' column to user_subtopic_progress table!")
        except sqlite3.OperationalError as e:
            if "duplicate column" in str(e):
                print("✓ Column 'status' already exists!")
            else:
                print(f"✗ Error: {e}")
                return False
        
        # Verify column was added
        cursor.execute("PRAGMA table_info(user_subtopic_progress)")
        columns = cursor.fetchall()
        print("\nTable structure:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        return True
        
    except Exception as e:
        print(f"✗ Database error: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    print("Running migration...")
    success = migrate()
    if success:
        print("\n✓ Migration completed successfully!")
    else:
        print("\n✗ Migration failed!")
