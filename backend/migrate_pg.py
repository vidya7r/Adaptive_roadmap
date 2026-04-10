#!/usr/bin/env python
"""
PostgreSQL migration to add 'status' column to user_subtopic_progress
Run from backend directory: python migrate_pg.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import engine
from sqlalchemy import text

def migrate_status_column():
    print("🔧 PostgreSQL Migration: Adding 'status' column\n")
    
    try:
        with engine.connect() as conn:
            # Check if column exists
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'user_subtopic_progress' 
                AND column_name = 'status'
            """))
            
            column_exists = result.fetchone() is not None
            
            if column_exists:
                print("✓ Column 'status' already exists!")
            else:
                print("⚙️  Adding 'status' column to user_subtopic_progress...")
                conn.execute(text("""
                    ALTER TABLE user_subtopic_progress 
                    ADD COLUMN status VARCHAR(50) DEFAULT 'pending'
                """))
                conn.commit()
                print("✓ Column added successfully!")
            
            # Show table structure
            print("\n📋 Current table structure:")
            result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_name = 'user_subtopic_progress'
                ORDER BY ordinal_position
            """))
            
            for row in result:
                nullable = "NULL" if row[2] == "YES" else "NOT NULL"
                print(f"  - {row[0]}: {row[1]} ({nullable})")
            
            print("\n✅ Migration complete!")
            return True
            
    except Exception as e:
        print(f"✗ Migration error: {str(e)}")
        print("\nManual SQL command to fix:")
        print("""
        ALTER TABLE user_subtopic_progress 
        ADD COLUMN status VARCHAR(50) DEFAULT 'pending';
        
        You can run this in pgAdmin or psql:
        psql -U postgres -d NDA -c "ALTER TABLE user_subtopic_progress ADD COLUMN status VARCHAR(50) DEFAULT 'pending';"
        """)
        return False

if __name__ == "__main__":
    try:
        success = migrate_status_column()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"✗ Fatal error: {e}")
        sys.exit(1)
