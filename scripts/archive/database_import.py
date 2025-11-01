"""
COLLEGE RECOMMENDATION SYSTEM - DATABASE IMPORT SCRIPT
Import enriched CSV data into PostgreSQL database
"""

import pandas as pd
import psycopg2
from psycopg2 import sql, extras
import numpy as np
from typing import Dict, List, Tuple
import sys
from datetime import datetime

# ============================================
# DATABASE CONFIGURATION
# ============================================

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'college_recommendation',  # Change this to your database name
    'user': 'postgres',  # Change this to your PostgreSQL username
    'password': 'Ayush@123'  # Change this to your PostgreSQL password
}

# File paths
COLLEGES_FILE = 'data/enriched_master_colleges.csv'
COURSES_FILE = 'data/enriched_master_courses.csv'


# ============================================
# DATABASE CONNECTION
# ============================================

def get_db_connection():
    """Create and return a database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Successfully connected to PostgreSQL database!")
        return conn
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        print("\n💡 Make sure to:")
        print("   1. Update DB_CONFIG with your PostgreSQL credentials")
        print("   2. Create the database: CREATE DATABASE college_recommendation;")
        print("   3. Run the database_schema.sql file first")
        sys.exit(1)


def test_connection():
    """Test database connection and schema"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Check if tables exist
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('colleges', 'courses', 'college_facilities', 'course_features')
        """)
        tables = [row[0] for row in cur.fetchall()]
        
        if len(tables) == 4:
            print(f"✅ All required tables found: {', '.join(tables)}")
        else:
            print(f"⚠️  Warning: Only found tables: {', '.join(tables)}")
            print("   Please run database_schema.sql first!")
            return False
            
        return True
    except Exception as e:
        print(f"❌ Error testing connection: {e}")
        return False
    finally:
        cur.close()
        conn.close()


# ============================================
# DATA LOADING
# ============================================

def load_csv_data():
    """Load enriched CSV files"""
    print("\n📂 Loading CSV files...")
    
    try:
        colleges_df = pd.read_csv(COLLEGES_FILE)
        courses_df = pd.read_csv(COURSES_FILE)
        
        print(f"✅ Loaded {len(colleges_df)} colleges")
        print(f"✅ Loaded {len(courses_df)} courses")
        
        return colleges_df, courses_df
    except Exception as e:
        print(f"❌ Error loading CSV files: {e}")
        sys.exit(1)


# ============================================
# DATA CLEANING FOR IMPORT
# ============================================

def clean_for_db(value):
    """Clean value for database insertion"""
    if pd.isna(value) or value == '' or value == 'Not Available':
        return None
    if isinstance(value, (np.integer, np.floating)):
        if np.isnan(value) or np.isinf(value):
            return None
    return value


def prepare_college_row(row: pd.Series) -> Dict:
    """Prepare college row for database insertion"""
    return {
        'college_name': clean_for_db(row.get('College Name')),  # Note: space not underscore
        'state': clean_for_db(row.get('State')),
        'city': clean_for_db(row.get('City')),
        'ownership': clean_for_db(row.get('College Type')),  # Fixed column name
        'college_type': clean_for_db(row.get('College Type')),
        'nirf_rank': clean_for_db(row.get('NIRF_Rank')),
        'naac_grade': clean_for_db(row.get('NAAC_Accreditation')),  # Fixed column name
        'naac_score': clean_for_db(row.get('Rating')),  # Using Rating as NAAC score
        'tier': clean_for_db(row.get('Affordability_Tier')),  # Fixed column name
        'affordability_score': clean_for_db(row.get('Affordability_Score')),
        'facility_score': clean_for_db(row.get('Facility_Score')),
        'quality_score': clean_for_db(row.get('Quality_Score')),
        'overall_score': clean_for_db(row.get('Overall_Score')),
        'website': clean_for_db(row.get('Website'))
    }


def prepare_facility_row(row: pd.Series, college_id: int) -> Dict:
    """Prepare facility row for database insertion"""
    # Convert Yes/No to boolean
    def to_bool(val):
        if pd.isna(val):
            return False
        return str(val).strip().lower() == 'yes'
    
    return {
        'college_id': college_id,
        'has_hostel': to_bool(row.get('Has_Hostel')),
        'has_library': to_bool(row.get('Has_Library')),
        'has_sports': to_bool(row.get('Has_Sports')),
        'has_gym': to_bool(row.get('Has_Gym')),
        'has_cafeteria': to_bool(row.get('Has_Cafeteria')),
        'has_medical': to_bool(row.get('Has_Medical')),
        'has_wifi': to_bool(row.get('Has_Wifi')),  # Note: capital W
        'has_lab': to_bool(row.get('Has_Lab')),
        'has_auditorium': to_bool(row.get('Has_Auditorium')),
        'has_transport': to_bool(row.get('Has_Transport')),
        'facilities_text': clean_for_db(row.get('Facilities'))
    }


def prepare_course_row(row: pd.Series, college_id: int) -> Dict:
    """Prepare course row for database insertion"""
    # Helper to convert Yes/No to boolean
    def to_bool(val):
        if pd.isna(val):
            return False
        return str(val).strip().lower() == 'yes'
    
    # Get category and set flags based on it
    category = str(row.get('Course_Category', '')).lower()
    
    return {
        'college_id': college_id,
        'course_name': clean_for_db(row.get('Course')),  # Fixed column name
        'degree_type': None,  # Not in CSV
        'duration_years': None,  # Not in CSV
        'total_fee': None,  # Not in CSV
        'fee_per_year': clean_for_db(row.get('Average_Fees')),  # Fixed column name
        'course_category': clean_for_db(row.get('Course_Category')),
        'is_cs_related': 'computer' in category or 'cs' in category or 'it' in category,
        'is_ai_ml': 'ai' in category or 'ml' in category or 'data' in category,
        'is_electronics': 'electronic' in category or 'ece' in category or 'eee' in category,
        'is_mechanical': 'mechanical' in category,
        'is_civil': 'civil' in category,
        'is_chemical': 'chemical' in category or 'biotech' in category,
        'is_aerospace': 'aero' in category
    }


# ============================================
# DATABASE IMPORT
# ============================================

def import_colleges(conn, colleges_df: pd.DataFrame) -> Dict[str, int]:
    """Import colleges and return mapping of college_name to college_id"""
    print("\n📥 Importing colleges...")
    cur = conn.cursor()
    college_id_map = {}
    
    insert_college_query = """
        INSERT INTO colleges (
            college_name, state, city, ownership, college_type,
            nirf_rank, naac_grade, naac_score, tier,
            affordability_score, facility_score, quality_score, overall_score,
            website
        ) VALUES (
            %(college_name)s, %(state)s, %(city)s, %(ownership)s, %(college_type)s,
            %(nirf_rank)s, %(naac_grade)s, %(naac_score)s, %(tier)s,
            %(affordability_score)s, %(facility_score)s, %(quality_score)s, %(overall_score)s,
            %(website)s
        ) RETURNING college_id
    """
    
    success_count = 0
    error_count = 0
    
    for idx, row in colleges_df.iterrows():
        try:
            college_data = prepare_college_row(row)
            cur.execute(insert_college_query, college_data)
            college_id = cur.fetchone()[0]
            college_id_map[row['College Name']] = college_id  # Fixed: space not underscore
            success_count += 1
            
            if success_count % 500 == 0:
                print(f"   Imported {success_count} colleges...")
                conn.commit()
                
        except Exception as e:
            error_count += 1
            print(f"   ⚠️  Error importing college '{row.get('College Name')}': {e}")
            conn.rollback()
            continue
    
    conn.commit()
    cur.close()
    
    print(f"✅ Successfully imported {success_count} colleges")
    if error_count > 0:
        print(f"⚠️  Failed to import {error_count} colleges")
    
    return college_id_map


def import_facilities(conn, colleges_df: pd.DataFrame, college_id_map: Dict[str, int]):
    """Import college facilities"""
    print("\n📥 Importing college facilities...")
    cur = conn.cursor()
    
    insert_facility_query = """
        INSERT INTO college_facilities (
            college_id, has_hostel, has_library, has_sports, has_gym,
            has_cafeteria, has_medical, has_wifi, has_lab,
            has_auditorium, has_transport, facilities_text
        ) VALUES (
            %(college_id)s, %(has_hostel)s, %(has_library)s, %(has_sports)s, %(has_gym)s,
            %(has_cafeteria)s, %(has_medical)s, %(has_wifi)s, %(has_lab)s,
            %(has_auditorium)s, %(has_transport)s, %(facilities_text)s
        )
    """
    
    success_count = 0
    error_count = 0
    
    for idx, row in colleges_df.iterrows():
        college_name = row['College Name']  # Fixed: space not underscore
        if college_name not in college_id_map:
            continue
            
        try:
            college_id = college_id_map[college_name]
            facility_data = prepare_facility_row(row, college_id)
            cur.execute(insert_facility_query, facility_data)
            success_count += 1
            
            if success_count % 500 == 0:
                print(f"   Imported {success_count} facility records...")
                conn.commit()
                
        except Exception as e:
            error_count += 1
            print(f"   ⚠️  Error importing facilities for '{college_name}': {e}")
            conn.rollback()
            continue
    
    conn.commit()
    cur.close()
    
    print(f"✅ Successfully imported {success_count} facility records")
    if error_count > 0:
        print(f"⚠️  Failed to import {error_count} facility records")


def import_courses(conn, courses_df: pd.DataFrame, college_id_map: Dict[str, int]):
    """Import courses"""
    print("\n📥 Importing courses...")
    cur = conn.cursor()
    
    insert_course_query = """
        INSERT INTO courses (
            college_id, course_name, degree_type, duration_years,
            total_fee, fee_per_year, course_category,
            is_cs_related, is_ai_ml, is_electronics, is_mechanical,
            is_civil, is_chemical, is_aerospace
        ) VALUES (
            %(college_id)s, %(course_name)s, %(degree_type)s, %(duration_years)s,
            %(total_fee)s, %(fee_per_year)s, %(course_category)s,
            %(is_cs_related)s, %(is_ai_ml)s, %(is_electronics)s, %(is_mechanical)s,
            %(is_civil)s, %(is_chemical)s, %(is_aerospace)s
        )
    """
    
    success_count = 0
    error_count = 0
    skipped_count = 0
    
    for idx, row in courses_df.iterrows():
        college_name = row.get('College_Name')
        
        # Skip if college not found
        if pd.isna(college_name) or college_name not in college_id_map:
            skipped_count += 1
            continue
            
        try:
            college_id = college_id_map[college_name]
            course_data = prepare_course_row(row, college_id)
            cur.execute(insert_course_query, course_data)
            success_count += 1
            
            if success_count % 500 == 0:
                print(f"   Imported {success_count} courses...")
                conn.commit()
                
        except Exception as e:
            error_count += 1
            print(f"   ⚠️  Error importing course '{row.get('Course_Name')}': {e}")
            conn.rollback()
            continue
    
    conn.commit()
    cur.close()
    
    print(f"✅ Successfully imported {success_count} courses")
    if error_count > 0:
        print(f"⚠️  Failed to import {error_count} courses")
    if skipped_count > 0:
        print(f"⚠️  Skipped {skipped_count} courses (college not found)")


# ============================================
# VERIFICATION
# ============================================

def verify_import(conn):
    """Verify the imported data"""
    print("\n🔍 Verifying imported data...")
    cur = conn.cursor()
    
    try:
        # Count records
        cur.execute("SELECT COUNT(*) FROM colleges")
        college_count = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM college_facilities")
        facility_count = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM courses")
        course_count = cur.fetchone()[0]
        
        print(f"\n📊 Import Summary:")
        print(f"   Colleges: {college_count:,}")
        print(f"   Facilities: {facility_count:,}")
        print(f"   Courses: {course_count:,}")
        
        # Sample queries
        print(f"\n🔍 Sample Queries:")
        
        # Top 5 colleges by overall score
        cur.execute("""
            SELECT college_name, tier, overall_score, nirf_rank 
            FROM colleges 
            ORDER BY overall_score DESC NULLS LAST 
            LIMIT 5
        """)
        print(f"\n   Top 5 Colleges by Overall Score:")
        for row in cur.fetchall():
            print(f"      {row[0]} | Tier: {row[1]} | Score: {row[2]:.2f} | NIRF: {row[3]}")
        
        # CS courses count
        cur.execute("SELECT COUNT(*) FROM courses WHERE is_cs_related = TRUE")
        cs_count = cur.fetchone()[0]
        print(f"\n   CS-Related Courses: {cs_count:,}")
        
        # Colleges with hostel
        cur.execute("SELECT COUNT(*) FROM college_facilities WHERE has_hostel = TRUE")
        hostel_count = cur.fetchone()[0]
        print(f"   Colleges with Hostel: {hostel_count:,}")
        
        print("\n✅ Database import completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during verification: {e}")
    finally:
        cur.close()


# ============================================
# MAIN EXECUTION
# ============================================

def main():
    """Main import process"""
    print("=" * 60)
    print("COLLEGE RECOMMENDATION SYSTEM - DATABASE IMPORT")
    print("=" * 60)
    
    # Step 1: Test connection
    if not test_connection():
        return
    
    # Step 2: Load CSV data
    colleges_df, courses_df = load_csv_data()
    
    # Step 3: Connect to database
    conn = get_db_connection()
    
    try:
        # Step 4: Import colleges (returns ID mapping)
        college_id_map = import_colleges(conn, colleges_df)
        
        # Step 5: Import facilities
        import_facilities(conn, colleges_df, college_id_map)
        
        # Step 6: Import courses
        import_courses(conn, courses_df, college_id_map)
        
        # Step 7: Verify import
        verify_import(conn)
        
    except Exception as e:
        print(f"\n❌ Fatal error during import: {e}")
        conn.rollback()
    finally:
        conn.close()
    
    print("\n" + "=" * 60)
    print("Import process completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
