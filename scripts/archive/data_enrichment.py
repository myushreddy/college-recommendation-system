"""
Data Enrichment Script
======================
This script enriches the master databases with:
1. Parsed facilities into searchable tags
2. Course categories (CS, AI/ML, Mechanical, Civil, etc.)
3. Computed fields:
   - Affordability Score (0-100)
   - Facility Score (0-100)
   - Quality Score (0-100)
   - Overall Ranking Score
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

print("\n" + "="*80)
print("DATA ENRICHMENT PROCESS")
print("="*80)
print("\nEnriching master databases with computed fields and categories...\n")

# ============================================================================
# LOAD DATA
# ============================================================================

print("Loading master databases...")
colleges_df = pd.read_csv('data/master_colleges.csv')
courses_df = pd.read_csv('data/master_courses.csv')

# Convert numeric columns to proper types
colleges_df['Rating'] = pd.to_numeric(colleges_df['Rating'], errors='coerce')
colleges_df['Average Fees'] = pd.to_numeric(colleges_df['Average Fees'], errors='coerce')
colleges_df['NIRF_Rank'] = pd.to_numeric(colleges_df['NIRF_Rank'], errors='coerce')
courses_df['Average_Fees'] = pd.to_numeric(courses_df['Average_Fees'], errors='coerce')
courses_df['Rating'] = pd.to_numeric(courses_df['Rating'], errors='coerce')
courses_df['NIRF_Rank'] = pd.to_numeric(courses_df['NIRF_Rank'], errors='coerce')

print(f"✓ Loaded {len(colleges_df):,} colleges")
print(f"✓ Loaded {len(courses_df):,} course entries")

# ============================================================================
# 1. PARSE FACILITIES INTO TAGS
# ============================================================================

print("\n" + "="*80)
print("1. PARSING FACILITIES INTO SEARCHABLE TAGS")
print("="*80)

def parse_facilities(facilities_str):
    """
    Parse facility string into individual tags
    Returns: comma-separated list of facility tags
    """
    if pd.isna(facilities_str) or facilities_str == 'Not Available':
        return 'Not Available'
    
    # Split by comma
    facilities = str(facilities_str).split(',')
    
    # Clean and standardize
    cleaned = []
    for f in facilities:
        f = f.strip()
        # Standardize common variations
        f = f.replace('Boys Hostel', 'Hostel')
        f = f.replace('Girls Hostel', 'Hostel')
        if f and f not in cleaned:
            cleaned.append(f)
    
    return ', '.join(cleaned) if cleaned else 'Not Available'


def count_facilities(facilities_str):
    """Count number of facilities"""
    if pd.isna(facilities_str) or facilities_str == 'Not Available':
        return 0
    return len([f for f in str(facilities_str).split(',') if f.strip()])


# Parse facilities
colleges_df['Facility_Tags'] = colleges_df['Facilities'].apply(parse_facilities)
colleges_df['Facility_Count'] = colleges_df['Facilities'].apply(count_facilities)

print(f"✓ Parsed facilities for {len(colleges_df)} colleges")
print(f"  Average facilities per college: {colleges_df['Facility_Count'].mean():.1f}")
print(f"  Max facilities: {colleges_df['Facility_Count'].max()}")

# Create individual facility flags for common amenities
facility_flags = {
    'Has_Hostel': 'Hostel',
    'Has_Gym': 'Gym',
    'Has_Library': 'Library',
    'Has_Sports': 'Sports',
    'Has_Cafeteria': 'Cafeteria',
    'Has_Medical': 'Medical',
    'Has_Wifi': 'Wifi',
    'Has_Lab': 'Laborator',  # Matches "Laboratory" or "Laboratories"
    'Has_Auditorium': 'Auditorium',
    'Has_Transport': 'Transport'
}

for flag_name, keyword in facility_flags.items():
    colleges_df[flag_name] = colleges_df['Facilities'].apply(
        lambda x: 'Yes' if pd.notna(x) and keyword.lower() in str(x).lower() else 'No'
    )

print(f"✓ Created {len(facility_flags)} facility flags")

# ============================================================================
# 2. CREATE COURSE CATEGORIES
# ============================================================================

print("\n" + "="*80)
print("2. CATEGORIZING COURSES")
print("="*80)

# Define course categories with keywords
COURSE_CATEGORIES = {
    'Computer Science & IT': [
        'computer science', 'information technology', 'it ', ' it,', 'software',
        'computer engineering', 'cse', 'computer application'
    ],
    'Artificial Intelligence & Data Science': [
        'artificial intelligence', 'ai ', 'machine learning', 'data science',
        'data analytics', 'ai and ml', 'ai & ml', 'ai/ml'
    ],
    'Electronics & Communication': [
        'electronics', 'communication', 'ece', 'telecommunication',
        'electronics and communication', 'vlsi', 'embedded'
    ],
    'Electrical & Power': [
        'electrical', 'eee', 'power', 'electrical and electronics'
    ],
    'Mechanical Engineering': [
        'mechanical', 'automobile', 'automotive', 'production',
        'industrial', 'manufacturing', 'robotics', 'mechatronics'
    ],
    'Civil Engineering': [
        'civil', 'construction', 'structural', 'transportation',
        'geotechnical', 'environmental engineering'
    ],
    'Chemical & Biotechnology': [
        'chemical', 'biotechnology', 'biomedical', 'biochemical',
        'bio technology', 'bio-technology', 'pharmaceutical'
    ],
    'Aerospace & Aeronautical': [
        'aerospace', 'aeronautical', 'aviation', 'aircraft'
    ],
    'Mining & Metallurgy': [
        'mining', 'metallurgy', 'metallurgical', 'materials', 'mineral'
    ],
    'Agriculture & Food Tech': [
        'agriculture', 'agricultural', 'food', 'food technology', 'food process'
    ],
    'Architecture & Planning': [
        'architecture', 'planning', 'urban', 'b.arch', 'barch'
    ],
    'Management & MBA': [
        'mba', 'management', 'business administration', 'bba'
    ],
    'Sciences': [
        'm.sc', 'msc', 'mathematics', 'physics', 'chemistry', 'life science'
    ],
    'Other Engineering': []  # Catch-all
}


def categorize_course(course_name):
    """Categorize a course into predefined categories"""
    if pd.isna(course_name):
        return 'Other Engineering'
    
    course_lower = str(course_name).lower()
    
    # Check each category
    for category, keywords in COURSE_CATEGORIES.items():
        if category == 'Other Engineering':
            continue
        for keyword in keywords:
            if keyword in course_lower:
                return category
    
    return 'Other Engineering'


# Categorize courses in course database
courses_df['Course_Category'] = courses_df['Course'].apply(categorize_course)

print(f"✓ Categorized {len(courses_df)} course entries")
print(f"\nCourse Category Distribution:")
category_counts = courses_df['Course_Category'].value_counts()
for cat, count in category_counts.head(10).items():
    print(f"   {cat}: {count} offerings")

# Add course categories to colleges based on their offerings
def get_course_categories(college_name):
    """Get all course categories offered by a college"""
    college_courses = courses_df[courses_df['College_Name'] == college_name]
    if len(college_courses) == 0:
        return 'Not Available'
    
    categories = college_courses['Course_Category'].unique()
    return ', '.join(sorted(categories))


colleges_df['Course_Categories_Offered'] = colleges_df['College Name'].apply(get_course_categories)

print(f"✓ Added course category information to colleges database")

# ============================================================================
# 3. COMPUTE AFFORDABILITY SCORE (0-100)
# ============================================================================

print("\n" + "="*80)
print("3. COMPUTING AFFORDABILITY SCORE")
print("="*80)

def calculate_affordability_score(fee):
    """
    Calculate affordability score (0-100)
    Lower fees = Higher score
    Scale: 0-50K=100, 50K-1L=80-90, 1L-2L=60-80, 2L-3L=40-60, 3L+=0-40
    """
    if pd.isna(fee) or fee == 0:
        return np.nan
    
    if fee <= 50000:
        return 100
    elif fee <= 100000:
        # 50K-100K: Score 90-80
        return 90 - ((fee - 50000) / 50000) * 10
    elif fee <= 200000:
        # 100K-200K: Score 80-60
        return 80 - ((fee - 100000) / 100000) * 20
    elif fee <= 300000:
        # 200K-300K: Score 60-40
        return 60 - ((fee - 200000) / 100000) * 20
    elif fee <= 500000:
        # 300K-500K: Score 40-20
        return 40 - ((fee - 300000) / 200000) * 20
    else:
        # 500K+: Score 20-0
        return max(0, 20 - ((fee - 500000) / 500000) * 20)


colleges_df['Affordability_Score'] = colleges_df['Average Fees'].apply(calculate_affordability_score)
courses_df['Affordability_Score'] = courses_df['Average_Fees'].apply(calculate_affordability_score)

print(f"✓ Calculated affordability scores")
print(f"  Colleges with affordability data: {colleges_df['Affordability_Score'].notna().sum():,}")
print(f"  Average affordability score: {colleges_df['Affordability_Score'].mean():.1f}/100")

# ============================================================================
# 4. COMPUTE FACILITY SCORE (0-100)
# ============================================================================

print("\n" + "="*80)
print("4. COMPUTING FACILITY SCORE")
print("="*80)

def calculate_facility_score(facility_count):
    """
    Calculate facility score (0-100)
    Based on number of facilities
    Scale: 0 facilities = 0, 15+ facilities = 100
    """
    if pd.isna(facility_count) or facility_count == 0:
        return 0
    
    # Linear scale: each facility adds ~6.67 points (15 facilities = 100)
    score = min(100, (facility_count / 15) * 100)
    return round(score, 1)


colleges_df['Facility_Score'] = colleges_df['Facility_Count'].apply(calculate_facility_score)

print(f"✓ Calculated facility scores")
print(f"  Average facility score: {colleges_df['Facility_Score'].mean():.1f}/100")

# ============================================================================
# 5. COMPUTE QUALITY SCORE (0-100)
# ============================================================================

print("\n" + "="*80)
print("5. COMPUTING QUALITY SCORE")
print("="*80)

def calculate_quality_score(row):
    """
    Calculate overall quality score (0-100) based on:
    - NIRF Rank (40% weight): Top 10=100, 11-50=80-99, 51-100=60-79, 101-200=40-59
    - Rating (30% weight): 0-5 scale converted to 0-100
    - Accreditations (20% weight): NBA+NAAC=100, One=50, None=0
    - College Type (10% weight): Government=100, Autonomous=80, Private=60
    """
    score = 0
    weights_used = 0
    
    # 1. NIRF Rank (40% weight)
    if pd.notna(row['NIRF_Rank']) and row['NIRF_Rank'] > 0:
        rank = row['NIRF_Rank']
        if rank <= 10:
            nirf_score = 100
        elif rank <= 50:
            nirf_score = 99 - ((rank - 10) / 40) * 19  # 99 to 80
        elif rank <= 100:
            nirf_score = 79 - ((rank - 50) / 50) * 19  # 79 to 60
        else:  # 101-200
            nirf_score = 59 - ((rank - 100) / 100) * 19  # 59 to 40
        score += nirf_score * 0.4
        weights_used += 0.4
    
    # 2. Rating (30% weight)
    if pd.notna(row['Rating']) and row['Rating'] > 0:
        # Convert 0-5 rating to 0-100 scale
        rating_score = (row['Rating'] / 5) * 100
        score += rating_score * 0.3
        weights_used += 0.3
    
    # 3. Accreditations (20% weight)
    accred_score = 0
    has_nba = row.get('NBA_Accreditation', 'Not Available') not in ['Not Available', 'No']
    has_naac = row.get('NAAC_Accreditation', 'Not Available') not in ['Not Available', 'No']
    
    if has_nba and has_naac:
        accred_score = 100
    elif has_nba or has_naac:
        accred_score = 50
    
    score += accred_score * 0.2
    weights_used += 0.2
    
    # 4. College Type (10% weight)
    college_type = str(row.get('College Type', '')).lower()
    if 'government' in college_type or 'public' in college_type:
        type_score = 100
    elif 'autonomous' in college_type:
        type_score = 80
    else:  # Private
        type_score = 60
    
    score += type_score * 0.1
    weights_used += 0.1
    
    # Normalize score based on weights used
    if weights_used > 0:
        final_score = (score / weights_used) * 1.0
        return round(min(100, final_score), 1)
    else:
        return np.nan


colleges_df['Quality_Score'] = colleges_df.apply(calculate_quality_score, axis=1)

print(f"✓ Calculated quality scores")
print(f"  Colleges with quality data: {colleges_df['Quality_Score'].notna().sum():,}")
print(f"  Average quality score: {colleges_df['Quality_Score'].mean():.1f}/100")

# Add quality score to courses (from college)
course_quality_map = colleges_df.set_index('College Name')['Quality_Score'].to_dict()
courses_df['Quality_Score'] = courses_df['College_Name'].map(course_quality_map)

# ============================================================================
# 6. COMPUTE OVERALL RANKING SCORE (0-100)
# ============================================================================

print("\n" + "="*80)
print("6. COMPUTING OVERALL RANKING SCORE")
print("="*80)

def calculate_overall_score(row):
    """
    Calculate overall ranking score (0-100) based on:
    - Quality Score (50% weight)
    - Facility Score (25% weight)
    - Affordability Score (25% weight)
    """
    scores = []
    weights = []
    
    if pd.notna(row['Quality_Score']):
        scores.append(row['Quality_Score'])
        weights.append(0.5)
    
    if pd.notna(row['Facility_Score']):
        scores.append(row['Facility_Score'])
        weights.append(0.25)
    
    if pd.notna(row.get('Affordability_Score')):
        scores.append(row['Affordability_Score'])
        weights.append(0.25)
    
    if len(scores) == 0:
        return np.nan
    
    # Weighted average
    total_weight = sum(weights)
    weighted_sum = sum(s * w for s, w in zip(scores, weights))
    
    return round(weighted_sum / total_weight, 1)


colleges_df['Overall_Score'] = colleges_df.apply(calculate_overall_score, axis=1)

# For courses, use a simpler calculation (no facility score)
def calculate_course_overall_score(row):
    """Calculate overall score for courses (no facility data)"""
    scores = []
    weights = []
    
    if pd.notna(row.get('Quality_Score')):
        scores.append(row['Quality_Score'])
        weights.append(0.6)  # Increased weight since no facility score
    
    if pd.notna(row.get('Affordability_Score')):
        scores.append(row['Affordability_Score'])
        weights.append(0.4)  # Increased weight
    
    if len(scores) == 0:
        return np.nan
    
    total_weight = sum(weights)
    weighted_sum = sum(s * w for s, w in zip(scores, weights))
    
    return round(weighted_sum / total_weight, 1)

courses_df['Overall_Score'] = courses_df.apply(calculate_course_overall_score, axis=1)

print(f"✓ Calculated overall ranking scores")
print(f"  Average overall score: {colleges_df['Overall_Score'].mean():.1f}/100")

# ============================================================================
# 7. ADD ADDITIONAL ENRICHMENT FIELDS
# ============================================================================

print("\n" + "="*80)
print("7. ADDING ADDITIONAL ENRICHMENT FIELDS")
print("="*80)

# Add affordability tier
def get_affordability_tier(fee):
    """Categorize college into affordability tiers"""
    if pd.isna(fee) or fee == 0:
        return 'Not Available'
    if fee <= 100000:
        return 'Budget-Friendly'
    elif fee <= 200000:
        return 'Affordable'
    elif fee <= 300000:
        return 'Moderate'
    elif fee <= 500000:
        return 'Premium'
    else:
        return 'Expensive'


colleges_df['Affordability_Tier'] = colleges_df['Average Fees'].apply(get_affordability_tier)
courses_df['Affordability_Tier'] = courses_df['Average_Fees'].apply(get_affordability_tier)

# Add quality tier
def get_quality_tier(score):
    """Categorize into quality tiers"""
    if pd.isna(score):
        return 'Not Rated'
    if score >= 80:
        return 'Excellent'
    elif score >= 60:
        return 'Good'
    elif score >= 40:
        return 'Average'
    else:
        return 'Below Average'


colleges_df['Quality_Tier'] = colleges_df['Quality_Score'].apply(get_quality_tier)
courses_df['Quality_Tier'] = courses_df['Quality_Score'].apply(get_quality_tier)

# Add ranking tier based on NIRF
def get_ranking_tier(rank):
    """Categorize into ranking tiers"""
    if pd.isna(rank) or rank == 0:
        return 'Not Ranked'
    if rank <= 10:
        return 'Top 10'
    elif rank <= 50:
        return 'Top 50'
    elif rank <= 100:
        return 'Top 100'
    else:
        return 'Top 200'


colleges_df['Ranking_Tier'] = colleges_df['NIRF_Rank'].apply(get_ranking_tier)
courses_df['Ranking_Tier'] = courses_df['NIRF_Rank'].apply(get_ranking_tier)

print(f"✓ Added tier categories (Affordability, Quality, Ranking)")

# ============================================================================
# 8. SAVE ENRICHED DATASETS
# ============================================================================

print("\n" + "="*80)
print("8. SAVING ENRICHED DATASETS")
print("="*80)

# Save enriched colleges
output_colleges = 'data/enriched_master_colleges.csv'
colleges_df.to_csv(output_colleges, index=False)
print(f"✓ SAVED: {output_colleges}")
print(f"  Rows: {len(colleges_df):,}, Columns: {len(colleges_df.columns)} (was 28, now {len(colleges_df.columns)})")

# Save enriched courses
output_courses = 'data/enriched_master_courses.csv'
courses_df.to_csv(output_courses, index=False)
print(f"✓ SAVED: {output_courses}")
print(f"  Rows: {len(courses_df):,}, Columns: {len(courses_df.columns)} (was 12, now {len(courses_df.columns)})")

# ============================================================================
# 9. GENERATE ENRICHMENT SUMMARY
# ============================================================================

print("\n" + "="*80)
print("ENRICHMENT SUMMARY")
print("="*80)

print(f"\n NEW FIELDS ADDED TO COLLEGES:")
new_college_fields = [
    'Facility_Tags', 'Facility_Count', 'Has_Hostel', 'Has_Gym', 'Has_Library',
    'Has_Sports', 'Has_Cafeteria', 'Has_Medical', 'Has_Wifi', 'Has_Lab',
    'Has_Auditorium', 'Has_Transport', 'Course_Categories_Offered',
    'Affordability_Score', 'Facility_Score', 'Quality_Score', 'Overall_Score',
    'Affordability_Tier', 'Quality_Tier', 'Ranking_Tier'
]
for field in new_college_fields:
    print(f"   ✓ {field}")

print(f"\n NEW FIELDS ADDED TO COURSES:")
new_course_fields = [
    'Course_Category', 'Affordability_Score', 'Quality_Score', 'Overall_Score',
    'Affordability_Tier', 'Quality_Tier', 'Ranking_Tier'
]
for field in new_course_fields:
    print(f"   ✓ {field}")

print(f"\n📈 SCORE DISTRIBUTIONS:")
print(f"   Affordability Score: {colleges_df['Affordability_Score'].mean():.1f}/100 (avg)")
print(f"   Facility Score: {colleges_df['Facility_Score'].mean():.1f}/100 (avg)")
print(f"   Quality Score: {colleges_df['Quality_Score'].mean():.1f}/100 (avg)")
print(f"   Overall Score: {colleges_df['Overall_Score'].mean():.1f}/100 (avg)")

print(f"\n🏆 TOP 10 COLLEGES BY OVERALL SCORE:")
top_10 = colleges_df.nlargest(10, 'Overall_Score')[['College Name', 'City', 'State', 'Overall_Score', 'NIRF_Rank']]
for idx, row in top_10.iterrows():
    nirf = f"(Rank {int(row['NIRF_Rank'])})" if pd.notna(row['NIRF_Rank']) else "(Not Ranked)"
    print(f"   {row['Overall_Score']:.1f}/100 - {row['College Name']}, {row['City']} {nirf}")

print(f"\n📊 AFFORDABILITY TIER DISTRIBUTION:")
tier_dist = colleges_df['Affordability_Tier'].value_counts()
for tier, count in tier_dist.items():
    print(f"   {tier}: {count:,} colleges ({count/len(colleges_df)*100:.1f}%)")

print(f"\n📊 QUALITY TIER DISTRIBUTION:")
quality_dist = colleges_df['Quality_Tier'].value_counts()
for tier, count in quality_dist.items():
    print(f"   {tier}: {count:,} colleges ({count/len(colleges_df)*100:.1f}%)")

print("\n" + "="*80)
print("✅ DATA ENRICHMENT COMPLETE!")
print("="*80)
print(f"\nNew enriched files created:")
print(f"   • enriched_master_colleges.csv - {len(colleges_df):,} colleges with {len(colleges_df.columns)} fields")
print(f"   • enriched_master_courses.csv - {len(courses_df):,} courses with {len(courses_df.columns)} fields")
print(f"\nNext steps:")
print(f"   1. Review enriched data")
print(f"   2. Design database schema")
print(f"   3. Import into database (PostgreSQL/MongoDB)")
print(f"   4. Build REST API")
print("\n" + "="*80 + "\n")
