"""
Fix Course and Facility Import with Fuzzy Matching
This script will properly match college names between CSVs and re-import all data
"""

import pandas as pd
import psycopg2
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import numpy as np
from typing import Dict, List, Tuple

# Database config
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'college_recommendation',
    'user': 'postgres',
    'password': 'Ayush@123'
}

print("=" * 100)
print("FIXING COURSE AND FACILITY IMPORT WITH FUZZY MATCHING")
print("=" * 100)

# Step 1: Load data
print("\n📂 Step 1: Loading CSV files...")
colleges_df = pd.read_csv('data/enriched_master_colleges.csv')
courses_df = pd.read_csv('data/enriched_master_courses.csv')

print(f"✅ Loaded {len(colleges_df)} colleges from CSV")
print(f"✅ Loaded {len(courses_df)} courses from CSV")

# Step 2: Get college names from database
print("\n📊 Step 2: Getting college names from database...")
conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

cur.execute("SELECT college_id, college_name, state, city FROM colleges")
db_colleges = cur.fetchall()
db_college_dict = {row[0]: {'name': row[1], 'state': row[2], 'city': row[3]} for row in db_colleges}

print(f"✅ Found {len(db_colleges)} colleges in database")

# Step 3: Create mapping functions
def normalize_name(name):
    """Normalize college name for better matching"""
    if pd.isna(name):
        return ""
    name = str(name).strip().lower()
    # Remove common variations
    name = name.replace('institute of technology', 'it')
    name = name.replace('college of engineering', 'college')
    name = name.replace('engineering college', 'college')
    name = name.replace('university', 'univ')
    name = name.replace(',', '')
    name = name.replace('.', '')
    name = name.replace('  ', ' ')
    return name

def find_best_match(csv_name, csv_state, csv_city, db_colleges_list):
    """Find best matching college from database"""
    best_match = None
    best_score = 0
    
    csv_name_norm = normalize_name(csv_name)
    
    for college_id, info in db_colleges_list.items():
        db_name = info['name']
        db_state = info['state']
        db_city = info['city']
        
        db_name_norm = normalize_name(db_name)
        
        # Calculate fuzzy match score
        name_score = fuzz.ratio(csv_name_norm, db_name_norm)
        
        # Bonus points for matching state/city
        state_match = 20 if (csv_state and db_state and str(csv_state).lower() == str(db_state).lower()) else 0
        city_match = 10 if (csv_city and db_city and str(csv_city).lower() == str(db_city).lower()) else 0
        
        total_score = name_score + state_match + city_match
        
        if total_score > best_score:
            best_score = total_score
            best_match = college_id
    
    return best_match, best_score

print("\n🔍 Step 3: Creating college name mappings...")

# Create mapping for colleges CSV
csv_to_db_mapping = {}
unmatched_colleges = []

for idx, row in colleges_df.iterrows():
    csv_name = row['College Name']
    csv_state = row.get('State')
    csv_city = row.get('City')
    
    college_id, score = find_best_match(csv_name, csv_state, csv_city, db_college_dict)
    
    if score >= 70:  # Threshold for acceptable match
        csv_to_db_mapping[csv_name] = college_id
    else:
        unmatched_colleges.append((csv_name, csv_state, score))
    
    if (idx + 1) % 500 == 0:
        print(f"   Processed {idx + 1} colleges...")

print(f"✅ Matched {len(csv_to_db_mapping)} colleges (threshold: 70%)")
print(f"⚠️  Could not match {len(unmatched_colleges)} colleges")

# Create mapping for courses CSV  
courses_to_db_mapping = {}
unmatched_courses = []

print("\n🔍 Step 4: Creating course name mappings...")

for idx, row in courses_df.iterrows():
    csv_name = row['College_Name']
    csv_state = row.get('State')
    csv_city = row.get('City')
    
    college_id, score = find_best_match(csv_name, csv_state, csv_city, db_college_dict)
    
    if score >= 70:
        courses_to_db_mapping[csv_name] = college_id
    else:
        unmatched_courses.append((csv_name, csv_state, score))
    
    if (idx + 1) % 500 == 0:
        print(f"   Processed {idx + 1} courses...")

print(f"✅ Matched {len(courses_to_db_mapping)} unique colleges in courses CSV")
print(f"⚠️  Could not match {len(set(unmatched_courses))} unique colleges")

# Step 4: Clear existing data
print("\n🗑️  Step 5: Clearing existing course and facility data...")
cur.execute("DELETE FROM courses")
cur.execute("DELETE FROM college_facilities")
conn.commit()
print("✅ Cleared existing data")

# Step 5: Import facilities with mapping
print("\n📥 Step 6: Importing facilities with corrected mappings...")

def to_bool(val):
    if pd.isna(val):
        return False
    return str(val).strip().lower() == 'yes'

insert_facility_query = """
    INSERT INTO college_facilities (
        college_id, has_hostel, has_library, has_sports, has_gym,
        has_cafeteria, has_medical, has_wifi, has_lab,
        has_auditorium, has_transport, facilities_text
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
"""

facility_success = 0
facility_errors = 0

for idx, row in colleges_df.iterrows():
    csv_name = row['College Name']
    
    if csv_name not in csv_to_db_mapping:
        continue
    
    college_id = csv_to_db_mapping[csv_name]
    
    try:
        facility_data = (
            college_id,
            to_bool(row.get('Has_Hostel')),
            to_bool(row.get('Has_Library')),
            to_bool(row.get('Has_Sports')),
            to_bool(row.get('Has_Gym')),
            to_bool(row.get('Has_Cafeteria')),
            to_bool(row.get('Has_Medical')),
            to_bool(row.get('Has_Wifi')),
            to_bool(row.get('Has_Lab')),
            to_bool(row.get('Has_Auditorium')),
            to_bool(row.get('Has_Transport')),
            row.get('Facilities') if not pd.isna(row.get('Facilities')) else None
        )
        
        cur.execute(insert_facility_query, facility_data)
        facility_success += 1
        
        if facility_success % 500 == 0:
            print(f"   Imported {facility_success} facilities...")
            conn.commit()
            
    except Exception as e:
        facility_errors += 1
        if facility_errors <= 5:
            print(f"   ⚠️  Error: {e}")
        conn.rollback()
        continue

conn.commit()
print(f"✅ Successfully imported {facility_success} facility records")
if facility_errors > 0:
    print(f"⚠️  Failed to import {facility_errors} facility records")

# Step 6: Import courses with mapping
print("\n📥 Step 7: Importing courses with corrected mappings...")

insert_course_query = """
    INSERT INTO courses (
        college_id, course_name, degree_type, duration_years,
        total_fee, fee_per_year, course_category,
        is_cs_related, is_ai_ml, is_electronics, is_mechanical,
        is_civil, is_chemical, is_aerospace
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
"""

def clean_for_db(value):
    if pd.isna(value) or value == '' or value == 'Not Available':
        return None
    if isinstance(value, (np.integer, np.floating)):
        if np.isnan(value) or np.isinf(value):
            return None
    return value

course_success = 0
course_errors = 0

for idx, row in courses_df.iterrows():
    csv_name = row['College_Name']
    
    if csv_name not in courses_to_db_mapping:
        continue
    
    college_id = courses_to_db_mapping[csv_name]
    
    try:
        category = str(row.get('Course_Category', '')).lower()
        
        course_data = (
            college_id,
            clean_for_db(row.get('Course')),
            None,  # degree_type
            None,  # duration_years
            None,  # total_fee
            clean_for_db(row.get('Average_Fees')),
            clean_for_db(row.get('Course_Category')),
            'computer' in category or 'cs' in category or 'it' in category or 'information technology' in category,
            'ai' in category or 'ml' in category or 'data' in category or 'artificial intelligence' in category,
            'electronic' in category or 'ece' in category or 'eee' in category,
            'mechanical' in category,
            'civil' in category,
            'chemical' in category or 'biotech' in category,
            'aero' in category
        )
        
        cur.execute(insert_course_query, course_data)
        course_success += 1
        
        if course_success % 500 == 0:
            print(f"   Imported {course_success} courses...")
            conn.commit()
            
    except Exception as e:
        course_errors += 1
        if course_errors <= 5:
            print(f"   ⚠️  Error: {e}")
        conn.rollback()
        continue

conn.commit()
print(f"✅ Successfully imported {course_success} courses")
if course_errors > 0:
    print(f"⚠️  Failed to import {course_errors} courses")

# Step 7: Verification
print("\n🔍 Step 8: Verifying import...")

cur.execute("SELECT COUNT(*) FROM colleges")
total_colleges = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM college_facilities")
total_facilities = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM courses")
total_courses = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM courses WHERE is_cs_related = TRUE")
cs_courses = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM college_facilities WHERE has_hostel = TRUE")
hostel_count = cur.fetchone()[0]

print("\n" + "=" * 100)
print("FINAL RESULTS")
print("=" * 100)
print(f"""
📊 Database Summary:
   Colleges:          {total_colleges:,}
   Facilities:        {total_facilities:,} ({total_facilities/total_colleges*100:.1f}% coverage)
   Courses:           {total_courses:,}
   CS Courses:        {cs_courses:,}
   With Hostel:       {hostel_count:,}

🎯 Improvement:
   Facilities Before: 277 → After: {total_facilities} (+{total_facilities-277})
   Courses Before:    11 → After: {total_courses} (+{total_courses-11})
   
✅ Import completed successfully!
""")

# Show some examples
print("📝 Sample Data:")
print("\nTop 5 CS Courses:")
cur.execute("""
    SELECT c.college_name, co.course_name, co.fee_per_year
    FROM courses co
    JOIN colleges c ON co.college_id = c.college_id
    WHERE co.is_cs_related = TRUE AND co.fee_per_year > 0
    ORDER BY co.fee_per_year
    LIMIT 5
""")
for row in cur.fetchall():
    print(f"   {row[0][:50]:50s} | {row[1][:30]:30s} | ₹{row[2]:,.0f}")

cur.close()
conn.close()

print("\n" + "=" * 100)
print("✅ ALL DONE! Database is now ready for the API!")
print("=" * 100)
