"""
College Data Cleaning Script
============================
This script cleans and standardizes data from three different college datasets:
1. engineering colleges in India.csv
2. Engineering.csv  
3. NIRF Ranking for Engineering Colleges 2024.csv

What this script does:
- Standardizes college names (removes extra spaces, fixes case)
- Handles missing values (replaces empty/null values with meaningful defaults)
- Cleans course names (removes line breaks, standardizes names)
- Normalizes fee structures (handles different formats, converts to numbers)
- Creates cleaned versions of each file
"""

import pandas as pd
import numpy as np
import re
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def standardize_college_name(name):
    """
    Standardizes college names by:
    - Converting to title case
    - Removing extra spaces
    - Removing special characters that might cause matching issues
    - Standardizing common abbreviations
    """
    if pd.isna(name) or name == '':
        return 'Unknown College'
    
    # Convert to string and strip whitespace
    name = str(name).strip()
    
    # Remove line breaks and extra spaces
    name = re.sub(r'\s+', ' ', name)
    name = re.sub(r'\n+', ' ', name)
    
    # Standardize common abbreviations
    replacements = {
        'Iit': 'IIT',
        'Nit': 'NIT',
        'Iiit': 'IIIT',
        'Bits': 'BITS',
        'Vit': 'VIT',
        'Mit': 'MIT',
        'Sri ': 'Sri ',
        'St ': 'St. ',
        'Dr ': 'Dr. ',
        'B.tech': 'B.Tech',
        'M.tech': 'M.Tech',
    }
    
    for old, new in replacements.items():
        name = re.sub(rf'\b{old}\b', new, name, flags=re.IGNORECASE)
    
    return name


def clean_course_name(course):
    """
    Cleans course names by:
    - Removing line breaks
    - Standardizing format
    - Removing extra spaces
    """
    if pd.isna(course) or course == '':
        return 'Not Specified'
    
    # Convert to string
    course = str(course)
    
    # Remove line breaks and extra spaces
    course = re.sub(r'\s+', ' ', course)
    course = re.sub(r'\n+', ' ', course)
    course = course.strip()
    
    # Standardize common course abbreviations
    course = re.sub(r'\bCSE\b', 'Computer Science and Engineering', course, flags=re.IGNORECASE)
    course = re.sub(r'\bECE\b', 'Electronics and Communication Engineering', course, flags=re.IGNORECASE)
    course = re.sub(r'\bEEE\b', 'Electrical and Electronics Engineering', course, flags=re.IGNORECASE)
    
    return course


def normalize_fee(fee):
    """
    Normalizes fee values by:
    - Converting to float
    - Handling missing values
    - Removing currency symbols
    """
    if pd.isna(fee) or fee == '' or fee == '-':
        return np.nan
    
    try:
        # If already a number
        if isinstance(fee, (int, float)):
            return float(fee)
        
        # Convert string to float
        fee_str = str(fee).strip()
        
        # Remove currency symbols and commas
        fee_str = re.sub(r'[₹$,]', '', fee_str)
        
        # Convert to float
        return float(fee_str)
    except:
        return np.nan


def handle_missing_values(df, column, default_value='Not Available'):
    """
    Handles missing values in a dataframe column
    """
    df[column] = df[column].fillna(default_value)
    df[column] = df[column].replace('', default_value)
    df[column] = df[column].replace('-', default_value)
    return df


# ============================================================================
# MAIN CLEANING FUNCTIONS
# ============================================================================

def clean_engineering_colleges_india():
    """
    Cleans the 'engineering colleges in India.csv' file
    This file has: College Name, Campus Size, Enrollments, Faculty, Rating, 
                   Courses, Facilities, City, State, Fees
    """
    print("\n" + "="*80)
    print("CLEANING: engineering colleges in India.csv")
    print("="*80)
    
    # Read the CSV
    df = pd.read_csv('data/engineering colleges in India.csv')
    print(f"✓ Loaded {len(df)} rows")
    
    # 1. Standardize College Names
    print("\n1. Standardizing college names...")
    df['College Name'] = df['College Name'].apply(standardize_college_name)
    print(f"   ✓ Cleaned {len(df)} college names")
    
    # 2. Handle Missing Values
    print("\n2. Handling missing values...")
    
    # Handle text columns
    text_columns = ['Genders Accepted', 'University', 'City', 'State', 'Country', 'College Type']
    for col in text_columns:
        if col in df.columns:
            df = handle_missing_values(df, col)
            missing_count = df[col].isna().sum()
            print(f"   ✓ {col}: {missing_count} missing values handled")
    
    # Handle numeric columns
    numeric_columns = ['Campus Size', 'Total Student Enrollments', 'Total Faculty', 
                       'Established Year', 'Rating']
    for col in numeric_columns:
        if col in df.columns:
            missing_before = df[col].isna().sum()
            df[col] = df[col].fillna(0)
            print(f"   ✓ {col}: {missing_before} missing values set to 0")
    
    # 3. Clean Course Names
    print("\n3. Cleaning course names...")
    if 'Courses' in df.columns:
        df['Courses'] = df['Courses'].apply(clean_course_name)
        print(f"   ✓ Cleaned course names (removed line breaks and standardized)")
    
    # 4. Normalize Fees
    print("\n4. Normalizing fee structure...")
    if 'Average Fees' in df.columns:
        df['Average Fees'] = df['Average Fees'].apply(normalize_fee)
        valid_fees = df['Average Fees'].notna().sum()
        print(f"   ✓ Normalized {valid_fees} fee values")
        print(f"   ✓ Fee range: ₹{df['Average Fees'].min():,.0f} to ₹{df['Average Fees'].max():,.0f}")
    
    # 5. Clean Facilities
    print("\n5. Cleaning facilities data...")
    if 'Facilities' in df.columns:
        df['Facilities'] = df['Facilities'].apply(lambda x: str(x).replace('\n', ', ') if pd.notna(x) else 'Not Available')
        print(f"   ✓ Cleaned facilities information")
    
    # Save cleaned data
    output_file = 'data/cleaned_engineering_colleges_india.csv'
    df.to_csv(output_file, index=False)
    print(f"\n✓ SAVED: {output_file}")
    print(f"  Rows: {len(df)}, Columns: {len(df.columns)}")
    
    return df


def clean_engineering_csv():
    """
    Cleans the 'Engineering.csv' file
    This file has: College ID, College Name, Region, State, District, 
                   Year of Establishment, Institute Type, Course (one per row)
    """
    print("\n" + "="*80)
    print("CLEANING: Engineering.csv")
    print("="*80)
    
    # Read the CSV with different encoding to handle special characters
    try:
        df = pd.read_csv('data/Engineering.csv', encoding='utf-8')
    except UnicodeDecodeError:
        print("   ⚠ UTF-8 encoding failed, trying Latin-1...")
        df = pd.read_csv('data/Engineering.csv', encoding='latin-1')
    
    print(f"✓ Loaded {len(df)} rows")
    
    # 1. Standardize College Names
    print("\n1. Standardizing college names...")
    df['college name'] = df['college name'].apply(standardize_college_name)
    print(f"   ✓ Cleaned {len(df)} college names")
    
    # 2. Handle Missing Values
    print("\n2. Handling missing values...")
    
    text_columns = ['Institute Region', 'State', 'District', 'Address', 
                    'Institute Type', 'College Category', 'University']
    for col in text_columns:
        if col in df.columns:
            df = handle_missing_values(df, col)
            print(f"   ✓ {col}: handled missing values")
    
    # 3. Clean Course Names
    print("\n3. Cleaning course names...")
    if 'Course' in df.columns:
        df['Course'] = df['Course'].apply(clean_course_name)
        unique_courses = df['Course'].nunique()
        print(f"   ✓ Cleaned course names")
        print(f"   ✓ Found {unique_courses} unique courses")
    
    # 4. Clean Year of Establishment
    print("\n4. Cleaning year of establishment...")
    if 'Year of Establishment' in df.columns:
        df['Year of Establishment'] = pd.to_numeric(df['Year of Establishment'], errors='coerce')
        df['Year of Establishment'] = df['Year of Establishment'].fillna(0).astype(int)
        valid_years = (df['Year of Establishment'] > 1800).sum()
        print(f"   ✓ Cleaned {valid_years} valid establishment years")
    
    # 5. Clean Accreditation columns
    print("\n5. Cleaning accreditation data...")
    accreditation_cols = ['NBA', 'NAAC', 'NIRF']
    for col in accreditation_cols:
        if col in df.columns:
            df[col] = df[col].fillna('Not Available')
            df[col] = df[col].replace('-', 'Not Available')
            print(f"   ✓ {col}: standardized values")
    
    # Save cleaned data
    output_file = 'data/cleaned_engineering.csv'
    df.to_csv(output_file, index=False)
    print(f"\n✓ SAVED: {output_file}")
    print(f"  Rows: {len(df)}, Columns: {len(df.columns)}")
    
    return df


def clean_nirf_rankings():
    """
    Cleans the 'NIRF Ranking for Engineering Colleges 2024.csv' file
    This file has: Sl No, Name, City, State, Rank
    """
    print("\n" + "="*80)
    print("CLEANING: NIRF Ranking for Engineering Colleges 2024.csv")
    print("="*80)
    
    # Read the CSV
    df = pd.read_csv('data/NIRF Ranking for Engineering Colleges 2024.csv')
    print(f"✓ Loaded {len(df)} rows")
    
    # 1. Standardize College Names
    print("\n1. Standardizing college names...")
    df['Name'] = df['Name'].apply(standardize_college_name)
    print(f"   ✓ Cleaned {len(df)} college names")
    
    # 2. Handle Missing Values
    print("\n2. Handling missing values...")
    df = handle_missing_values(df, 'City')
    df = handle_missing_values(df, 'State')
    print(f"   ✓ Handled missing values in City and State")
    
    # 3. Clean Rank column
    print("\n3. Cleaning rank data...")
    if 'Rank' in df.columns:
        df['Rank'] = pd.to_numeric(df['Rank'], errors='coerce')
        df['Rank'] = df['Rank'].fillna(999).astype(int)
        top_10 = df[df['Rank'] <= 10]['Name'].tolist()
        print(f"   ✓ Cleaned rank values")
        print(f"   ✓ Top 3 colleges: {', '.join(top_10[:3])}")
    
    # Save cleaned data
    output_file = 'data/cleaned_nirf_rankings.csv'
    df.to_csv(output_file, index=False)
    print(f"\n✓ SAVED: {output_file}")
    print(f"  Rows: {len(df)}, Columns: {len(df.columns)}")
    
    return df


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main function to clean all datasets
    """
    print("\n" + "="*80)
    print("COLLEGE DATA CLEANING PROCESS")
    print("="*80)
    print("\nThis script will clean and standardize all three datasets.")
    print("Cleaned files will be saved with 'cleaned_' prefix.\n")
    
    try:
        # Clean each dataset
        df1 = clean_engineering_colleges_india()
        df2 = clean_engineering_csv()
        df3 = clean_nirf_rankings()
        
        # Summary
        print("\n" + "="*80)
        print("CLEANING COMPLETE!")
        print("="*80)
        print("\n📊 Summary:")
        print(f"  • cleaned_engineering_colleges_india.csv: {len(df1)} rows")
        print(f"  • cleaned_engineering.csv: {len(df2)} rows")
        print(f"  • cleaned_nirf_rankings.csv: {len(df3)} rows")
        print(f"\n  Total records processed: {len(df1) + len(df2) + len(df3):,}")
        
        print("\n✅ All datasets cleaned successfully!")
        print("\nNext steps:")
        print("  1. Review the cleaned CSV files in the 'data' folder")
        print("  2. Run data merging to combine all three datasets")
        print("  3. Build the database schema")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
