"""
Comprehensive Database Audit - Check What's Missing
This script checks every field and identifies missing/incomplete data
"""

import pandas as pd
import psycopg2
from collections import defaultdict

# Database config
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'college_recommendation',
    'user': 'postgres',
    'password': 'Ayush@123'
}

print("=" * 100)
print("COMPREHENSIVE DATABASE AUDIT - CHECKING WHAT'S MISSING")
print("=" * 100)

# Connect to database
conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

# Load CSV files for comparison
print("\n📂 Loading CSV files for comparison...")
colleges_csv = pd.read_csv('data/enriched_master_colleges.csv')
courses_csv = pd.read_csv('data/enriched_master_courses.csv')

print(f"✅ CSV Data: {len(colleges_csv)} colleges, {len(courses_csv)} courses")

# ============================================
# PART 1: COLLEGES TABLE AUDIT
# ============================================
print("\n" + "=" * 100)
print("PART 1: COLLEGES TABLE AUDIT")
print("=" * 100)

# Get all colleges from database
cur.execute("""
    SELECT college_id, college_name, state, city, ownership, college_type,
           nirf_rank, naac_grade, naac_score, tier,
           affordability_score, facility_score, quality_score, overall_score,
           website
    FROM colleges
""")
db_colleges = cur.fetchall()

print(f"\n📊 Database has {len(db_colleges)} colleges")

# Check for NULL values in important fields
cur.execute("""
    SELECT 
        COUNT(*) as total,
        COUNT(college_name) as has_name,
        COUNT(state) as has_state,
        COUNT(city) as has_city,
        COUNT(ownership) as has_ownership,
        COUNT(college_type) as has_type,
        COUNT(nirf_rank) as has_nirf,
        COUNT(naac_grade) as has_naac_grade,
        COUNT(naac_score) as has_naac_score,
        COUNT(tier) as has_tier,
        COUNT(affordability_score) as has_affordability,
        COUNT(facility_score) as has_facility_score,
        COUNT(quality_score) as has_quality_score,
        COUNT(overall_score) as has_overall_score,
        COUNT(website) as has_website
    FROM colleges
""")
college_stats = cur.fetchone()

print("\n📋 College Field Coverage:")
fields = [
    ('College Name', college_stats[1], college_stats[0]),
    ('State', college_stats[2], college_stats[0]),
    ('City', college_stats[3], college_stats[0]),
    ('Ownership', college_stats[4], college_stats[0]),
    ('College Type', college_stats[5], college_stats[0]),
    ('NIRF Rank', college_stats[6], college_stats[0]),
    ('NAAC Grade', college_stats[7], college_stats[0]),
    ('NAAC Score', college_stats[8], college_stats[0]),
    ('Tier', college_stats[9], college_stats[0]),
    ('Affordability Score', college_stats[10], college_stats[0]),
    ('Facility Score', college_stats[11], college_stats[0]),
    ('Quality Score', college_stats[12], college_stats[0]),
    ('Overall Score', college_stats[13], college_stats[0]),
    ('Website', college_stats[14], college_stats[0]),
]

for field_name, count, total in fields:
    percentage = (count / total * 100) if total > 0 else 0
    status = "✅" if percentage > 80 else "⚠️" if percentage > 50 else "❌"
    print(f"   {status} {field_name:25s}: {count:4d} / {total:4d} ({percentage:5.1f}%)")

# Check what's in CSV but not in DB
print("\n🔍 Checking colleges in CSV but not in database...")
csv_colleges = set(colleges_csv['College Name'].dropna().str.strip())
db_college_names = set([row[1] for row in db_colleges])

missing_colleges = []
for csv_college in csv_colleges:
    # Check if any DB college is a close match
    found = False
    csv_lower = csv_college.lower()
    for db_college in db_college_names:
        if csv_lower == db_college.lower():
            found = True
            break
    if not found:
        missing_colleges.append(csv_college)

print(f"⚠️  Found {len(missing_colleges)} colleges in CSV but not in database")
if len(missing_colleges) > 0:
    print(f"   First 10 missing colleges:")
    for college in sorted(missing_colleges)[:10]:
        print(f"      - {college}")

# ============================================
# PART 2: FACILITIES TABLE AUDIT
# ============================================
print("\n" + "=" * 100)
print("PART 2: FACILITIES TABLE AUDIT")
print("=" * 100)

cur.execute("SELECT COUNT(*) FROM college_facilities")
facilities_count = cur.fetchone()[0]
colleges_count = len(db_colleges)

print(f"\n📊 Facilities Coverage:")
print(f"   Colleges in DB:       {colleges_count}")
print(f"   Facility Records:     {facilities_count}")
print(f"   Coverage:             {facilities_count/colleges_count*100:.1f}%")
print(f"   Missing:              {colleges_count - facilities_count}")

if facilities_count < colleges_count:
    print(f"\n❌ ISSUE: {colleges_count - facilities_count} colleges missing facility data!")
    
    # Find which colleges are missing facilities
    cur.execute("""
        SELECT c.college_id, c.college_name, c.state
        FROM colleges c
        LEFT JOIN college_facilities f ON c.college_id = f.college_id
        WHERE f.facility_id IS NULL
        LIMIT 20
    """)
    missing_facilities = cur.fetchall()
    
    print(f"   First 20 colleges without facilities:")
    for row in missing_facilities:
        print(f"      - {row[1]} ({row[2]})")

# Check facility flags distribution
cur.execute("""
    SELECT 
        COUNT(*) as total,
        SUM(CASE WHEN has_hostel THEN 1 ELSE 0 END) as hostel,
        SUM(CASE WHEN has_library THEN 1 ELSE 0 END) as library,
        SUM(CASE WHEN has_sports THEN 1 ELSE 0 END) as sports,
        SUM(CASE WHEN has_gym THEN 1 ELSE 0 END) as gym,
        SUM(CASE WHEN has_cafeteria THEN 1 ELSE 0 END) as cafeteria,
        SUM(CASE WHEN has_medical THEN 1 ELSE 0 END) as medical,
        SUM(CASE WHEN has_wifi THEN 1 ELSE 0 END) as wifi,
        SUM(CASE WHEN has_lab THEN 1 ELSE 0 END) as lab,
        SUM(CASE WHEN has_auditorium THEN 1 ELSE 0 END) as auditorium,
        SUM(CASE WHEN has_transport THEN 1 ELSE 0 END) as transport
    FROM college_facilities
""")
facility_flags = cur.fetchone()

if facility_flags[0] > 0:
    print(f"\n📋 Facility Flags (out of {facility_flags[0]} records):")
    facilities = [
        ('Hostel', facility_flags[1]),
        ('Library', facility_flags[2]),
        ('Sports', facility_flags[3]),
        ('Gym', facility_flags[4]),
        ('Cafeteria', facility_flags[5]),
        ('Medical', facility_flags[6]),
        ('WiFi', facility_flags[7]),
        ('Lab', facility_flags[8]),
        ('Auditorium', facility_flags[9]),
        ('Transport', facility_flags[10]),
    ]
    for name, count in facilities:
        percentage = (count / facility_flags[0] * 100) if facility_flags[0] > 0 else 0
        print(f"   {name:15s}: {count:3d} ({percentage:5.1f}%)")

# ============================================
# PART 3: COURSES TABLE AUDIT
# ============================================
print("\n" + "=" * 100)
print("PART 3: COURSES TABLE AUDIT")
print("=" * 100)

cur.execute("SELECT COUNT(*) FROM courses")
courses_count = cur.fetchone()[0]

print(f"\n📊 Courses Coverage:")
print(f"   Courses in CSV:       {len(courses_csv)}")
print(f"   Courses in DB:        {courses_count}")
print(f"   Import Rate:          {courses_count/len(courses_csv)*100:.1f}%")
print(f"   Missing:              {len(courses_csv) - courses_count}")

# Check course field coverage
cur.execute("""
    SELECT 
        COUNT(*) as total,
        COUNT(course_name) as has_name,
        COUNT(degree_type) as has_degree,
        COUNT(duration_years) as has_duration,
        COUNT(total_fee) as has_total_fee,
        COUNT(fee_per_year) as has_fee_per_year,
        COUNT(course_category) as has_category
    FROM courses
""")
course_stats = cur.fetchone()

print(f"\n📋 Course Field Coverage:")
course_fields = [
    ('Course Name', course_stats[1], course_stats[0]),
    ('Degree Type', course_stats[2], course_stats[0]),
    ('Duration Years', course_stats[3], course_stats[0]),
    ('Total Fee', course_stats[4], course_stats[0]),
    ('Fee Per Year', course_stats[5], course_stats[0]),
    ('Course Category', course_stats[6], course_stats[0]),
]

for field_name, count, total in course_fields:
    percentage = (count / total * 100) if total > 0 else 0
    status = "✅" if percentage > 80 else "⚠️" if percentage > 50 else "❌"
    missing = total - count
    print(f"   {status} {field_name:20s}: {count:4d} / {total:4d} ({percentage:5.1f}%) - Missing: {missing}")

# Check course category distribution
cur.execute("""
    SELECT course_category, COUNT(*) as count
    FROM courses
    WHERE course_category IS NOT NULL
    GROUP BY course_category
    ORDER BY count DESC
""")
categories = cur.fetchall()

print(f"\n📊 Course Category Distribution ({len(categories)} categories):")
for cat, count in categories:
    print(f"   {cat:35s}: {count:4d} courses")

# Check course flags
cur.execute("""
    SELECT 
        SUM(CASE WHEN is_cs_related THEN 1 ELSE 0 END) as cs,
        SUM(CASE WHEN is_ai_ml THEN 1 ELSE 0 END) as ai_ml,
        SUM(CASE WHEN is_electronics THEN 1 ELSE 0 END) as electronics,
        SUM(CASE WHEN is_mechanical THEN 1 ELSE 0 END) as mechanical,
        SUM(CASE WHEN is_civil THEN 1 ELSE 0 END) as civil,
        SUM(CASE WHEN is_chemical THEN 1 ELSE 0 END) as chemical,
        SUM(CASE WHEN is_aerospace THEN 1 ELSE 0 END) as aerospace
    FROM courses
""")
course_flags = cur.fetchone()

print(f"\n📋 Course Type Flags:")
print(f"   CS/IT Related:        {course_flags[0]:4d} courses")
print(f"   AI/ML:                {course_flags[1]:4d} courses")
print(f"   Electronics:          {course_flags[2]:4d} courses")
print(f"   Mechanical:           {course_flags[3]:4d} courses")
print(f"   Civil:                {course_flags[4]:4d} courses")
print(f"   Chemical/Biotech:     {course_flags[5]:4d} courses")
print(f"   Aerospace:            {course_flags[6]:4d} courses")

# Check which colleges have courses
cur.execute("""
    SELECT 
        COUNT(DISTINCT college_id) as colleges_with_courses,
        (SELECT COUNT(*) FROM colleges) as total_colleges
    FROM courses
""")
college_course_stats = cur.fetchone()

print(f"\n📊 College-Course Relationship:")
print(f"   Total Colleges:            {college_course_stats[1]}")
print(f"   Colleges with Courses:     {college_course_stats[0]}")
print(f"   Colleges without Courses:  {college_course_stats[1] - college_course_stats[0]}")
print(f"   Coverage:                  {college_course_stats[0]/college_course_stats[1]*100:.1f}%")

# ============================================
# PART 4: NIRF COVERAGE AUDIT
# ============================================
print("\n" + "=" * 100)
print("PART 4: NIRF RANKED COLLEGES AUDIT")
print("=" * 100)

# Check NIRF in CSV
nirf_in_csv = colleges_csv[colleges_csv['NIRF_Rank'].notna()]
print(f"\n📊 NIRF Coverage:")
print(f"   NIRF colleges in CSV:     {len(nirf_in_csv)}")

# Check NIRF in DB
cur.execute("SELECT COUNT(*) FROM colleges WHERE nirf_rank IS NOT NULL")
nirf_in_db = cur.fetchone()[0]
print(f"   NIRF colleges in DB:      {nirf_in_db}")

# Check top 50
cur.execute("SELECT COUNT(*) FROM colleges WHERE nirf_rank <= 50")
top_50 = cur.fetchone()[0]
print(f"   Top 50 NIRF in DB:        {top_50}")

# Check top 100
cur.execute("SELECT COUNT(*) FROM colleges WHERE nirf_rank <= 100")
top_100 = cur.fetchone()[0]
print(f"   Top 100 NIRF in DB:       {top_100}")

# Find missing NIRF ranks
cur.execute("""
    SELECT DISTINCT nirf_rank 
    FROM colleges 
    WHERE nirf_rank <= 200 
    ORDER BY nirf_rank
""")
present_ranks = set([row[0] for row in cur.fetchall()])
all_ranks = set(range(1, 201))
missing_ranks = sorted(all_ranks - present_ranks)

print(f"   Missing from Top 200:     {len(missing_ranks)} ranks")
if len(missing_ranks) > 0 and len(missing_ranks) <= 20:
    print(f"   Missing ranks: {missing_ranks}")
elif len(missing_ranks) > 20:
    print(f"   First 20 missing: {missing_ranks[:20]}")

# ============================================
# PART 5: DATA QUALITY ISSUES
# ============================================
print("\n" + "=" * 100)
print("PART 5: DATA QUALITY ISSUES")
print("=" * 100)

# Check for invalid scores (should be 0-100)
cur.execute("""
    SELECT 
        COUNT(*) as total,
        SUM(CASE WHEN affordability_score < 0 OR affordability_score > 100 THEN 1 ELSE 0 END) as bad_afford,
        SUM(CASE WHEN facility_score < 0 OR facility_score > 100 THEN 1 ELSE 0 END) as bad_facility,
        SUM(CASE WHEN quality_score < 0 OR quality_score > 100 THEN 1 ELSE 0 END) as bad_quality,
        SUM(CASE WHEN overall_score < 0 OR overall_score > 100 THEN 1 ELSE 0 END) as bad_overall
    FROM colleges
    WHERE affordability_score IS NOT NULL OR facility_score IS NOT NULL 
       OR quality_score IS NOT NULL OR overall_score IS NOT NULL
""")
score_issues = cur.fetchone()

print(f"\n📋 Score Validation (should be 0-100):")
print(f"   Invalid Affordability Scores:  {score_issues[1]}")
print(f"   Invalid Facility Scores:       {score_issues[2]}")
print(f"   Invalid Quality Scores:        {score_issues[3]}")
print(f"   Invalid Overall Scores:        {score_issues[4]}")

# Check for courses with zero fees (might be missing data)
cur.execute("""
    SELECT COUNT(*) 
    FROM courses 
    WHERE fee_per_year = 0 OR fee_per_year IS NULL
""")
zero_fee_courses = cur.fetchone()[0]
print(f"\n📋 Course Fee Issues:")
print(f"   Courses with zero/null fees:   {zero_fee_courses} / {courses_count} ({zero_fee_courses/courses_count*100:.1f}%)")

# ============================================
# FINAL SUMMARY
# ============================================
print("\n" + "=" * 100)
print("FINAL AUDIT SUMMARY")
print("=" * 100)

issues_found = []
recommendations = []

# Check colleges
if college_stats[9] < college_stats[0] * 0.5:  # tier coverage < 50%
    issues_found.append(f"❌ Tier field only {college_stats[9]/college_stats[0]*100:.1f}% populated")
    recommendations.append("Re-import college tier classifications")

if college_stats[6] < 200:  # NIRF coverage
    issues_found.append(f"⚠️  Only {college_stats[6]} NIRF ranked colleges (expected ~200)")
    recommendations.append("Add missing NIRF ranked colleges")

# Check facilities
if facilities_count < colleges_count * 0.5:
    issues_found.append(f"❌ Only {facilities_count/colleges_count*100:.1f}% colleges have facility data")
    recommendations.append("Fix facility import to cover all colleges")

# Check courses
if courses_count < len(courses_csv) * 0.5:
    issues_found.append(f"⚠️  Only {courses_count/len(courses_csv)*100:.1f}% of courses imported")
    recommendations.append("Improve course matching algorithm")

if college_course_stats[0] < college_course_stats[1] * 0.3:
    issues_found.append(f"❌ Only {college_course_stats[0]/college_course_stats[1]*100:.1f}% colleges have course data")
    recommendations.append("Map courses to more colleges")

print(f"\n{'='*100}")
print(f"ISSUES FOUND: {len(issues_found)}")
print(f"{'='*100}")

if len(issues_found) == 0:
    print("✅ No major issues found! Database is in great shape!")
else:
    for issue in issues_found:
        print(f"{issue}")

print(f"\n{'='*100}")
print(f"RECOMMENDATIONS: {len(recommendations)}")
print(f"{'='*100}")

if len(recommendations) == 0:
    print("✅ No recommendations. Database is production-ready!")
else:
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec}")

# Calculate overall health score
total_checks = 10
passed_checks = 0

if college_stats[1] == college_stats[0]: passed_checks += 1  # All have names
if college_stats[2] > college_stats[0] * 0.9: passed_checks += 1  # 90%+ have state
if college_stats[13] > college_stats[0] * 0.8: passed_checks += 1  # 80%+ have overall_score
if facilities_count > colleges_count * 0.05: passed_checks += 1  # At least 5% have facilities
if courses_count > 1000: passed_checks += 1  # Have substantial courses
if course_stats[6] > course_stats[0] * 0.8: passed_checks += 1  # 80%+ courses categorized
if course_flags[0] > 500: passed_checks += 1  # 500+ CS courses
if college_stats[6] > 100: passed_checks += 1  # 100+ NIRF colleges
if college_course_stats[0] > 300: passed_checks += 1  # 300+ colleges have courses
if zero_fee_courses < courses_count * 0.3: passed_checks += 1  # Less than 30% missing fees

health_score = (passed_checks / total_checks) * 100

print(f"\n{'='*100}")
print(f"DATABASE HEALTH SCORE: {health_score:.0f}% ({passed_checks}/{total_checks} checks passed)")
print(f"{'='*100}")

if health_score >= 80:
    print("✅ EXCELLENT! Database is production-ready!")
elif health_score >= 60:
    print("⚠️  GOOD! Database is usable but needs some fixes")
else:
    print("❌ NEEDS WORK! Several issues need to be addressed")

cur.close()
conn.close()

print("\n" + "=" * 100)
print("AUDIT COMPLETE!")
print("=" * 100)
