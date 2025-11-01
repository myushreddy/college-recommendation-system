"""
FIXED Data Merging Script
==========================
Fixes the fuzzy matching issues by:
1. Using stricter matching threshold (95%+)
2. Checking city/state for confirmation
3. Adding unmatched NIRF colleges to master database
"""

import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz, process
import warnings
warnings.filterwarnings('ignore')

print("\n" + "="*80)
print("FIXED DATA MERGING PROCESS")
print("="*80)
print("\nThis will create corrected master databases with proper NIRF matching.\n")

# Load all datasets
df1 = pd.read_csv('data/cleaned_engineering_colleges_india.csv')
df2 = pd.read_csv('data/cleaned_engineering.csv')
df3 = pd.read_csv('data/cleaned_nirf_rankings.csv')

print(f"✓ Datasets loaded")

# Start with Dataset 1 as base
master_df = df1.copy()

# Add new columns
master_df['NIRF_Rank'] = np.nan
master_df['Institute_Region'] = 'Not Available'
master_df['District'] = 'Not Available'
master_df['Address'] = 'Not Available'
master_df['Institute_Type'] = 'Not Available'
master_df['College_Category'] = 'Not Available'
master_df['Website'] = 'Not Available'
master_df['NBA_Accreditation'] = 'Not Available'
master_df['NAAC_Accreditation'] = 'Not Available'
master_df['NIRF_Status'] = 'Not Available'
master_df['Women_Institute'] = 'Not Available'
master_df['Courses_Offered'] = master_df['Courses']
master_df['Data_Sources'] = 'Dataset1'

print("✓ Schema created")

#=============================================================================
# IMPROVED FUZZY MATCHING FUNCTION
#=============================================================================

def find_best_match_improved(nirf_name, nirf_city, nirf_state, master_df, threshold=95):
    """
    Improved matching that considers name + location
    """
    # Try exact match first
    exact = master_df[master_df['College Name'] == nirf_name]
    if len(exact) > 0:
        return exact.iloc[0]['College Name'], 100, "exact"
    
    # Get all college names
    master_names = master_df['College Name'].tolist()
    
    # Find best name match
    result = process.extractOne(nirf_name, master_names, scorer=fuzz.token_sort_ratio)
    
    if result and result[1] >= threshold:
        matched_name = result[0]
        score = result[1]
        
        # Verify with location
        matched_colleges = master_df[master_df['College Name'] == matched_name]
        
        # Check if any match on city or state
        for idx, row in matched_colleges.iterrows():
            if (pd.notna(nirf_city) and pd.notna(row['City']) and 
                str(nirf_city).lower() in str(row['City']).lower()):
                return matched_name, score, "name+city"
            if (pd.notna(nirf_state) and pd.notna(row['State']) and 
                str(nirf_state).lower() == str(row['State']).lower()):
                return matched_name, score, "name+state"
        
        # If no location match, return anyway but flag it
        return matched_name, score, "name_only"
    
    return None, 0, "not_found"

#=============================================================================
# MERGE NIRF RANKINGS WITH IMPROVED MATCHING
#=============================================================================

print("\n" + "="*80)
print("MERGING NIRF RANKINGS (IMPROVED)")
print("="*80)

matched_colleges = []
unmatched_colleges = []

for idx, row in df3.iterrows():
    nirf_name = row['Name']
    nirf_city = row.get('City', '')
    nirf_state = row.get('State', '')
    nirf_rank = row['Rank']
    
    # Try to find match
    matched_name, score, match_type = find_best_match_improved(
        nirf_name, nirf_city, nirf_state, master_df, threshold=95
    )
    
    if matched_name and score >= 95:
        # Good match found
        mask = master_df['College Name'] == matched_name
        master_df.loc[mask, 'NIRF_Rank'] = nirf_rank
        
        # Update data sources
        current_sources = master_df.loc[mask, 'Data_Sources'].values[0]
        if 'Dataset3' not in current_sources:
            master_df.loc[mask, 'Data_Sources'] = current_sources + ',Dataset3'
        
        matched_colleges.append({
            'NIRF_Name': nirf_name,
            'Matched_Name': matched_name,
            'Score': score,
            'Type': match_type,
            'Rank': nirf_rank
        })
    else:
        # No good match - this college will be added separately
        unmatched_colleges.append({
            'Name': nirf_name,
            'City': nirf_city,
            'State': nirf_state,
            'Rank': nirf_rank
        })

print(f"\n✓ Matching Results:")
print(f"   - Matched with high confidence: {len(matched_colleges)}")
print(f"   - Unmatched (will be added): {len(unmatched_colleges)}")

# Show matched colleges
print(f"\n📊 Sample Matched Colleges (first 5):")
for match in matched_colleges[:5]:
    print(f"   Rank {match['Rank']:3d}: {match['NIRF_Name']}")
    print(f"      → {match['Matched_Name']} ({match['Score']}%, {match['Type']})")

#=============================================================================
# ADD UNMATCHED NIRF COLLEGES TO MASTER
#=============================================================================

print(f"\n" + "="*80)
print("ADDING UNMATCHED NIRF COLLEGES")
print("="*80)

print(f"\n🏆 Adding {len(unmatched_colleges)} NIRF-ranked colleges that weren't in Dataset 1:")

for college in unmatched_colleges:
    # Create new row with NIRF data
    new_row = {
        'College Name': college['Name'],
        'Genders Accepted': 'Not Available',
        'Campus Size': 0,
        'Total Student Enrollments': 0,
        'Total Faculty': 0,
        'Established Year': 0,
        'Rating': 0,
        'University': 'Not Available',
        'Courses': 'Not Available',
        'Facilities': 'Not Available',
        'City': college['City'],
        'State': college['State'],
        'Country': 'India',
        'College Type': 'Not Available',
        'Average Fees': 0,
        'NIRF_Rank': college['Rank'],
        'Institute_Region': 'Not Available',
        'District': 'Not Available',
        'Address': 'Not Available',
        'Institute_Type': 'Not Available',
        'College_Category': 'Not Available',
        'Website': 'Not Available',
        'NBA_Accreditation': 'Not Available',
        'NAAC_Accreditation': 'Not Available',
        'NIRF_Status': 'Not Available',
        'Women_Institute': 'Not Available',
        'Courses_Offered': 'Not Available',
        'Data_Sources': 'Dataset3'
    }
    
    # Add to master
    master_df = pd.concat([master_df, pd.DataFrame([new_row])], ignore_index=True)
    
    print(f"   Rank {int(college['Rank']):3d}: {college['Name']}")

print(f"\n✓ Master database now has {len(master_df)} colleges")

#=============================================================================
# MERGE DATASET 2 (SAME AS BEFORE)
#=============================================================================

print(f"\n" + "="*80)
print("MERGING COURSE-LEVEL DATA (Dataset 2)")
print("="*80)

df2_colleges = df2['college name'].unique()
matches_found_d2 = 0
master_colleges_list = master_df['College Name'].tolist()

for college_name in df2_colleges:
    result = process.extractOne(college_name, master_colleges_list, scorer=fuzz.token_sort_ratio)
    
    if result and result[1] >= 80:
        matched_name = result[0]
        college_data = df2[df2['college name'] == college_name].iloc[0]
        
        mask = master_df['College Name'] == matched_name
        
        # Update fields
        if master_df.loc[mask, 'Institute_Region'].values[0] == 'Not Available':
            master_df.loc[mask, 'Institute_Region'] = college_data.get('Institute Region', 'Not Available')
        
        if master_df.loc[mask, 'District'].values[0] == 'Not Available':
            master_df.loc[mask, 'District'] = college_data.get('District', 'Not Available')
        
        if master_df.loc[mask, 'Address'].values[0] == 'Not Available':
            master_df.loc[mask, 'Address'] = college_data.get('Address', 'Not Available')
        
        if master_df.loc[mask, 'Institute_Type'].values[0] == 'Not Available':
            master_df.loc[mask, 'Institute_Type'] = college_data.get('Institute Type', 'Not Available')
        
        if master_df.loc[mask, 'College_Category'].values[0] == 'Not Available':
            master_df.loc[mask, 'College_Category'] = college_data.get('College Category', 'Not Available')
        
        if master_df.loc[mask, 'Website'].values[0] == 'Not Available':
            master_df.loc[mask, 'Website'] = college_data.get('Website', 'Not Available')
        
        if master_df.loc[mask, 'NBA_Accreditation'].values[0] == 'Not Available':
            master_df.loc[mask, 'NBA_Accreditation'] = college_data.get('NBA', 'Not Available')
        
        if master_df.loc[mask, 'NAAC_Accreditation'].values[0] == 'Not Available':
            master_df.loc[mask, 'NAAC_Accreditation'] = college_data.get('NAAC', 'Not Available')
        
        if master_df.loc[mask, 'NIRF_Status'].values[0] == 'Not Available':
            master_df.loc[mask, 'NIRF_Status'] = college_data.get('NIRF', 'Not Available')
        
        if master_df.loc[mask, 'Women_Institute'].values[0] == 'Not Available':
            master_df.loc[mask, 'Women_Institute'] = college_data.get('Women Institute', 'Not Available')
        
        current_sources = master_df.loc[mask, 'Data_Sources'].values[0]
        if 'Dataset2' not in current_sources:
            master_df.loc[mask, 'Data_Sources'] = current_sources + ',Dataset2'
        
        matches_found_d2 += 1

print(f"\n✓ Matched {matches_found_d2} colleges from Dataset 2")

#=============================================================================
# CREATE COURSE-LEVEL DATABASE
#=============================================================================

print(f"\n" + "="*80)
print("CREATING COURSE-LEVEL DATABASE")
print("="*80)

course_level_data = []

for idx, row in df2.iterrows():
    college_name = row['college name']
    course_name = row['Course']
    
    result = process.extractOne(college_name, master_colleges_list, scorer=fuzz.token_sort_ratio)
    
    if result and result[1] >= 80:
        matched_name = result[0]
        college_info = master_df[master_df['College Name'] == matched_name].iloc[0]
        
        course_entry = {
            'College_Name': matched_name,
            'Course': course_name,
            'City': college_info['City'],
            'State': college_info['State'],
            'University': college_info['University'],
            'Average_Fees': college_info['Average Fees'],
            'Rating': college_info['Rating'],
            'NIRF_Rank': college_info['NIRF_Rank'],
            'Institute_Type': college_info['Institute_Type'],
            'NBA_Accreditation': college_info['NBA_Accreditation'],
            'NAAC_Accreditation': college_info['NAAC_Accreditation'],
            'Website': college_info['Website']
        }
        
        course_level_data.append(course_entry)

courses_df = pd.DataFrame(course_level_data)

print(f"✓ Created course database with {len(courses_df)} entries")

#=============================================================================
# SAVE FIXED DATASETS
#=============================================================================

print(f"\n" + "="*80)
print("SAVING FIXED DATASETS")
print("="*80)

# Save fixed versions
master_df.to_csv('data/master_colleges_fixed.csv', index=False)
courses_df.to_csv('data/master_courses_fixed.csv', index=False)

print(f"\n✓ SAVED: data/master_colleges_fixed.csv ({len(master_df)} colleges)")
print(f"✓ SAVED: data/master_courses_fixed.csv ({len(courses_df)} course entries)")

#=============================================================================
# VERIFICATION
#=============================================================================

print(f"\n" + "="*80)
print("VERIFICATION OF FIXED DATA")
print("="*80)

# Check if top NIRF colleges are present
print(f"\n🏆 Top 10 NIRF Ranked Colleges in Fixed Master:")
top_10 = master_df[master_df['NIRF_Rank'].notna()].nsmallest(10, 'NIRF_Rank')
for idx, row in top_10.iterrows():
    print(f"   {int(row['NIRF_Rank']):3d}. {row['College Name']}")
    print(f"        {row['City']}, {row['State']} | Source: {row['Data_Sources']}")

# Check duplicates
duplicates = master_df['College Name'].duplicated().sum()
print(f"\n📊 Duplicate Check:")
print(f"   - Duplicate college names: {duplicates}")
print(f"   - This is NORMAL (different branches/cities)")

print(f"\n" + "="*80)
print("✅ FIXED DATA MERGING COMPLETE!")
print("="*80)
print(f"\nNew files created:")
print(f"   • master_colleges_fixed.csv - {len(master_df)} colleges (includes all NIRF)")
print(f"   • master_courses_fixed.csv - {len(courses_df)} course entries")
print("\n" + "="*80 + "\n")
