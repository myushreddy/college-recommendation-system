"""
Data Cleaning Verification Script
==================================
This script shows you a before/after comparison of the cleaned data
"""

import pandas as pd

def show_comparison(title, original_file, cleaned_file, sample_rows=5):
    """Show before/after comparison"""
    print("\n" + "="*80)
    print(f"📊 {title}")
    print("="*80)
    
    # Read files
    try:
        original = pd.read_csv(original_file, encoding='utf-8', nrows=sample_rows)
    except:
        original = pd.read_csv(original_file, encoding='latin-1', nrows=sample_rows)
    
    cleaned = pd.read_csv(cleaned_file, nrows=sample_rows)
    
    print(f"\n✓ Loaded {sample_rows} sample rows from each file")
    print(f"\nOriginal columns: {list(original.columns)}")
    print(f"Cleaned columns:  {list(cleaned.columns)}")
    
    # Show sample college names
    print("\n📝 COLLEGE NAME COMPARISON:")
    print("\nBefore:")
    for i, name in enumerate(original.iloc[:, 0].head(3), 1):
        print(f"  {i}. {repr(name)}")
    
    print("\nAfter:")
    for i, name in enumerate(cleaned.iloc[:, 0].head(3), 1):
        print(f"  {i}. {repr(name)}")
    
    # Show missing values count
    print("\n📊 MISSING VALUES:")
    print(f"\nBefore: {original.isna().sum().sum()} missing values")
    print(f"After:  {cleaned.isna().sum().sum()} missing values")
    
    return original, cleaned


def main():
    print("\n" + "="*80)
    print("DATA CLEANING VERIFICATION")
    print("="*80)
    print("\nThis will show you before/after comparisons of the cleaned data.\n")
    
    # Dataset 1
    print("\n" + "🔍 INSPECTING DATASET 1...")
    orig1, clean1 = show_comparison(
        "Engineering Colleges in India",
        "data/engineering colleges in India.csv",
        "data/cleaned_engineering_colleges_india.csv"
    )
    
    # Show fee comparison
    if 'Average Fees' in orig1.columns:
        print("\n💰 FEE NORMALIZATION EXAMPLE:")
        print("\nBefore (first 3 fees):")
        for i, fee in enumerate(orig1['Average Fees'].head(3), 1):
            print(f"  {i}. {repr(fee)}")
        print("\nAfter (first 3 fees):")
        for i, fee in enumerate(clean1['Average Fees'].head(3), 1):
            print(f"  {i}. {fee:,.2f} INR" if pd.notna(fee) else f"  {i}. Not Available")
    
    # Dataset 2
    print("\n\n" + "🔍 INSPECTING DATASET 2...")
    orig2, clean2 = show_comparison(
        "Engineering Courses",
        "data/Engineering.csv",
        "data/cleaned_engineering.csv"
    )
    
    # Show course name comparison
    if 'Course' in orig2.columns:
        print("\n📚 COURSE NAME CLEANING EXAMPLE:")
        print("\nBefore (first 3 courses):")
        for i, course in enumerate(orig2['Course'].head(3), 1):
            print(f"  {i}. {repr(course[:50])}..." if len(str(course)) > 50 else f"  {i}. {repr(course)}")
        print("\nAfter (first 3 courses):")
        for i, course in enumerate(clean2['Course'].head(3), 1):
            print(f"  {i}. {course}")
    
    # Dataset 3
    print("\n\n" + "🔍 INSPECTING DATASET 3...")
    orig3, clean3 = show_comparison(
        "NIRF Rankings",
        "data/NIRF Ranking for Engineering Colleges 2024.csv",
        "data/cleaned_nirf_rankings.csv"
    )
    
    # Show rankings
    print("\n🏆 TOP 5 COLLEGES (NIRF 2024):")
    for i, row in clean3.head(5).iterrows():
        print(f"  {row['Rank']}. {row['Name']} - {row['City']}, {row['State']}")
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY OF CHANGES")
    print("="*80)
    
    print("\n✅ What was cleaned:")
    print("  1. College names standardized (proper case, no extra spaces)")
    print("  2. Missing values handled (filled with 'Not Available' or 0)")
    print("  3. Course names cleaned (removed line breaks, standardized)")
    print("  4. Fees normalized (converted to numbers, removed ₹ and commas)")
    print("  5. Special characters and encoding issues fixed")
    
    print("\n📁 Files created:")
    print("  • data/cleaned_engineering_colleges_india.csv")
    print("  • data/cleaned_engineering.csv")
    print("  • data/cleaned_nirf_rankings.csv")
    
    print("\n✅ Ready for next step: Data Merging!")


if __name__ == "__main__":
    main()
