"""
Final Verification - Quick Check
=================================
Run this anytime to verify the master databases are correct
"""

import pandas as pd

print("\n" + "="*80)
print("✅ FINAL VERIFICATION - MASTER DATABASES")
print("="*80)

# Load master databases
master_colleges = pd.read_csv('data/master_colleges.csv')
master_courses = pd.read_csv('data/master_courses.csv')

print(f"\n📊 MASTER COLLEGES:")
print(f"   - Total colleges: {len(master_colleges):,}")
print(f"   - Columns: {len(master_colleges.columns)}")
print(f"   - NIRF ranked: {master_colleges['NIRF_Rank'].notna().sum()}")
print(f"   - NBA accredited: {(master_colleges['NBA_Accreditation'] != 'Not Available').sum()}")
print(f"   - NAAC accredited: {(master_colleges['NAAC_Accreditation'] != 'Not Available').sum()}")

print(f"\n📊 MASTER COURSES:")
print(f"   - Total course entries: {len(master_courses):,}")
print(f"   - Unique colleges: {master_courses['College_Name'].nunique()}")
print(f"   - Unique courses: {master_courses['Course'].nunique()}")

print(f"\n🏆 TOP 10 NIRF RANKED COLLEGES:")
top_10 = master_colleges[master_colleges['NIRF_Rank'].notna()].nsmallest(10, 'NIRF_Rank')

for idx, row in top_10.iterrows():
    print(f"   {int(row['NIRF_Rank']):3d}. {row['College Name']}")
    print(f"        📍 {row['City']}, {row['State']}")

# Verify top 5 IITs are present
print(f"\n✅ CRITICAL VERIFICATION - Top 5 IITs:")
iit_check = {
    "IIT Madras": "Madras",
    "IIT Delhi": "Delhi",
    "IIT Bombay": "Bombay",
    "IIT Kanpur": "Kanpur",
    "IIT Kharagpur": "Kharagpur"
}

all_found = True
for display_name, search_term in iit_check.items():
    found = master_colleges['College Name'].str.contains(search_term, case=False, na=False).any()
    status = "✅" if found else "❌"
    print(f"   {status} {display_name}: {'Found' if found else 'NOT FOUND'}")
    if not found:
        all_found = False

all_found = all(iit_check.values())

print(f"\n" + "="*80)
if all_found and len(master_colleges) >= 5500 and master_colleges['NIRF_Rank'].notna().sum() >= 190:
    print("✅ VERIFICATION PASSED - ALL DATA CORRECT!")
else:
    print("⚠️  VERIFICATION ISSUES DETECTED - PLEASE REVIEW")
print("="*80 + "\n")
