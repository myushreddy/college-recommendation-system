"""
Simple test to check database connectivity.
"""
import sys
sys.path.insert(0, 'C:/Users/mayus/Documents/GitHub/college-recommendation-system/backend')

from app.core.database import engine, SessionLocal
from sqlalchemy import text

try:
    # Test connection
    with engine.connect() as connection:
        result = connection.execute(text("SELECT COUNT(*) FROM colleges"))
        count = result.scalar()
        print(f"Database connection successful!")
        print(f" Total colleges in database: {count}")
        
    # Test session
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT college_name FROM colleges LIMIT 5"))
        colleges = result.fetchall()
        print(f"\nSample colleges:")
        for i, (name,) in enumerate(colleges, 1):
            print(f"   {i}. {name}")
    finally:
        db.close()
        
    print("\n All database tests passed!")
    
except Exception as e:
    print(f" Database error: {e}")
    import traceback
    traceback.print_exc()
