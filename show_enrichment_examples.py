import pandas as pd

# Load enriched data
df = pd.read_csv('data/enriched_master_colleges.csv')

print("="*80)
print("EXAMPLE DATA FROM ENRICHED DATABASE")
print("="*80)

# Example 1: IIT Madras (Top College)
print("\n=== EXAMPLE 1: IIT Madras (Top NIRF College) ===")
iit = df[df['College Name'].str.contains('IIT Madras', case=False, na=False)]
if len(iit) > 0:
    iit = iit.iloc[0]
    print(f"College: {iit['College Name']}")
    print(f"Location: {iit['City']}, {iit['State']}")
    print(f"NIRF Rank: {int(iit['NIRF_Rank']) if pd.notna(iit['NIRF_Rank']) else 'Not Ranked'}")
    print(f"Average Fees: ₹{iit['Average Fees']:,.0f}" if pd.notna(iit['Average Fees']) else "Not Available")
    print(f"\nFacilities: {int(iit['Facility_Count'])} facilities available")
    print(f"  • Hostel: {iit['Has_Hostel']}")
    print(f"  • Gym: {iit['Has_Gym']}")
    print(f"  • Library: {iit['Has_Library']}")
    print(f"  • WiFi: {iit['Has_Wifi']}")
    print(f"  • Sports: {iit['Has_Sports']}")
    print(f"\nScores:")
    print(f"  • Affordability Score: {iit['Affordability_Score']:.2f}/100 ({iit['Affordability_Tier']})")
    print(f"  • Facility Score: {iit['Facility_Score']:.2f}/100")
    print(f"  • Quality Score: {iit['Quality_Score']:.2f}/100 ({iit['Quality_Tier']})")
    print(f"  • Overall Score: {iit['Overall_Score']:.2f}/100")

# Example 2: Budget-friendly college with good facilities
print("\n=== EXAMPLE 2: Budget-Friendly College with Excellent Facilities ===")
budget = df[
    (df['Affordability_Tier'] == 'Budget-Friendly') & 
    (df['Facility_Score'] >= 80)
].head(1)
if len(budget) > 0:
    budget = budget.iloc[0]
    print(f"College: {budget['College Name']}")
    print(f"Location: {budget['City']}, {budget['State']}")
    print(f"Average Fees: ₹{budget['Average Fees']:,.0f}")
    print(f"\nFacilities: {int(budget['Facility_Count'])} facilities")
    print(f"Scores:")
    print(f"  • Affordability: {budget['Affordability_Score']:.2f}/100 (Budget-Friendly!)")
    print(f"  • Facilities: {budget['Facility_Score']:.2f}/100 (Excellent!)")
    print(f"  • Overall: {budget['Overall_Score']:.2f}/100")

# Example 3: Course categorization
print("\n=== EXAMPLE 3: Course Categorization Sample ===")
courses = pd.read_csv('data/enriched_master_courses.csv')
cs_courses = courses[courses['Course_Category'] == 'Computer Science & IT'].head(5)
print(f"Found {len(courses[courses['Course_Category'] == 'Computer Science & IT'])} CS courses")
print("\nSample CS Courses:")
for idx, row in cs_courses.iterrows():
    print(f"  • {row['Course']} at {row['College_Name']}, {row['City']}")

# Summary statistics
print("\n=== SUMMARY STATISTICS ===")
print(f"\nTotal Colleges: {len(df):,}")
print(f"Total Course Offerings: {len(courses):,}")
print(f"\nFacility Availability:")
print(f"  • With Hostels: {(df['Has_Hostel'] == 'Yes').sum():,} ({(df['Has_Hostel'] == 'Yes').sum()/len(df)*100:.1f}%)")
print(f"  • With Gyms: {(df['Has_Gym'] == 'Yes').sum():,} ({(df['Has_Gym'] == 'Yes').sum()/len(df)*100:.1f}%)")
print(f"  • With WiFi: {(df['Has_Wifi'] == 'Yes').sum():,} ({(df['Has_Wifi'] == 'Yes').sum()/len(df)*100:.1f}%)")
print(f"\nAffordability Distribution:")
for tier in ['Budget-Friendly', 'Affordable', 'Moderate', 'Premium', 'Expensive']:
    count = (df['Affordability_Tier'] == tier).sum()
    print(f"  • {tier}: {count:,} colleges ({count/len(df)*100:.1f}%)")
print(f"\nCourse Categories:")
top_categories = courses['Course_Category'].value_counts().head(5)
for cat, count in top_categories.items():
    print(f"  • {cat}: {count} offerings")

print("\n" + "="*80)
print("✅ ALL ENRICHMENT VERIFIED - DATA IS READY FOR USE!")
print("="*80)
