#!/usr/bin/env python
"""
Setup script to ensure database is properly initialized with status column
Run from backend directory: python setup_db.py
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import engine
from app import models
import sqlite3

def setup_database():
    print("🔧 Setting up database...\n")
    
    # Create all tables if they don't exist
    print("✓ Creating tables...")
    models.Base.metadata.create_all(bind=engine)
    
    # Check and add status column if missing
    db_path = os.path.join(os.path.dirname(__file__), 'app', 'database.db')
    if os.path.exists(db_path):
        print(f"✓ Database found at: {db_path}")
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Check table structure
            print("\n📋 Checking user_subtopic_progress table structure...")
            cursor.execute("PRAGMA table_info(user_subtopic_progress)")
            columns = cursor.fetchall()
            column_names = [col[1] for col in columns]
            
            print("Current columns:")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
            
            # Add status column if missing
            if 'status' not in column_names:
                print("\n⚙️  Adding 'status' column...")
                try:
                    cursor.execute("""
                        ALTER TABLE user_subtopic_progress 
                        ADD COLUMN status VARCHAR(50) DEFAULT 'pending'
                    """)
                    conn.commit()
                    print("✓ 'status' column added successfully!")
                except sqlite3.OperationalError as e:
                    print(f"✗ Could not add column: {e}")
            else:
                print("\n✓ 'status' column already exists!")
            
            conn.close()
            
        except Exception as e:
            print(f"✗ Error checking database: {e}")
            return False
    else:
        print(f"✗ Database not found at: {db_path}")
        return False
    
    print("\n✅ Database setup complete!")
    return True

if __name__ == "__main__":
    try:
        setup_database()
    except Exception as e:
        print(f"✗ Setup failed: {e}")
        sys.exit(1)
