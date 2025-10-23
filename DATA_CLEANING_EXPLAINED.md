# Data Cleaning Process - Detailed Explanation

## 🎯 What is Data Cleaning?

Data cleaning is the process of preparing raw data for analysis by:
- Fixing errors
- Removing inconsistencies
- Standardizing formats
- Handling missing values

Think of it like organizing a messy room - you're making everything neat and consistent!

---

## 📋 What the Script Does (Step by Step)

### **1. Standardizing College Names**

**Problem:** College names are written differently across datasets
```
"Indian Institute Of Technology Madras"
"Indian Institute of Technology Madras"
"IIT MADRAS"
```

**Solution:** The `standardize_college_name()` function:
```python
def standardize_college_name(name):
    # Remove extra spaces
    name = re.sub(r'\s+', ' ', name)  # "IIT  Madras" → "IIT Madras"
    
    # Remove line breaks
    name = re.sub(r'\n+', ' ', name)  # Removes \n characters
    
    # Standardize abbreviations
    name = name.replace('Iit', 'IIT')  # "Iit" → "IIT"
```

**Example:**
```
Before: "indian  institute\nof technology  madras"
After:  "Indian Institute of Technology Madras"
```

---

### **2. Handling Missing Values**

**Problem:** Some cells are empty, have "-", or "N/A"
```
College Name: "IIT Delhi"
City: ""           ← Empty!
State: "-"         ← Dash!
Rating: NaN        ← Not a number!
```

**Solution:** The `handle_missing_values()` function:
```python
# For text columns: Replace with "Not Available"
df['City'].fillna('Not Available')

# For numbers: Replace with 0 or leave as NaN
df['Rating'].fillna(0)
```

**Example:**
```
Before:
  College Name: ABC College, City: "", Fees: ""
  
After:
  College Name: ABC College, City: "Not Available", Fees: 0
```

---

### **3. Cleaning Course Names**

**Problem:** Course names have line breaks and inconsistent formats
```
"COMPUTER SCIENCE &\n ENGINEERING"
"Computer Science And Engineering"
"CSE"
```

**Solution:** The `clean_course_name()` function:
```python
# Remove line breaks
course = re.sub(r'\n+', ' ', course)

# Standardize abbreviations
course = course.replace('CSE', 'Computer Science and Engineering')
```

**Example:**
```
Before: "COMPUTER SCIENCE &\n ENGINEERING"
After:  "Computer Science and Engineering"
```

---

### **4. Normalizing Fee Structures**

**Problem:** Fees are in different formats
```
"₹350,600.0"
"350600"
"-"
""
```

**Solution:** The `normalize_fee()` function:
```python
# Remove currency symbols and commas
fee = re.sub(r'[₹$,]', '', fee)  # "₹350,600" → "350600"

# Convert to number
fee = float(fee)  # "350600" → 350600.0
```

**Example:**
```
Before: "₹3,50,600.00"
After:  350600.0
```

---

## 🔍 Understanding Each Dataset Cleaning

### **Dataset 1: `engineering colleges in India.csv`**

**What it has:** Detailed college information with facilities, fees, ratings

**Cleaning steps:**
1. ✅ Standardize 5,447 college names
2. ✅ Handle missing values in City, State, University
3. ✅ Clean course names (remove \n, standardize)
4. ✅ Normalize fees (convert ₹350,600 → 350600.0)
5. ✅ Clean facilities list (format consistently)

**Output:** `cleaned_engineering_colleges_india.csv`

---

### **Dataset 2: `Engineering.csv`**

**What it has:** Course-level data with accreditations (NBA, NAAC, NIRF)

**Cleaning steps:**
1. ✅ Standardize 5,818 college names (one row per course!)
2. ✅ Handle missing values in Region, District, Address
3. ✅ Clean course names (very important here!)
4. ✅ Standardize Year of Establishment (some have "-")
5. ✅ Clean NBA, NAAC, NIRF columns

**Output:** `cleaned_engineering.csv`

---

### **Dataset 3: `NIRF Ranking for Engineering Colleges 2024.csv`**

**What it has:** Official government rankings of top 200 colleges

**Cleaning steps:**
1. ✅ Standardize 202 college names
2. ✅ Handle missing values in City, State
3. ✅ Clean rank data (ensure all are numbers)

**Output:** `cleaned_nirf_rankings.csv`

---

## 💻 How to Run the Script

### **Step 1: Install Required Libraries**
```bash
pip install pandas numpy
```

### **Step 2: Run the Script**
```bash
python data_cleaning.py
```

### **Step 3: Check Output**
You'll see three new files in the `data` folder:
- ✅ `cleaned_engineering_colleges_india.csv`
- ✅ `cleaned_engineering.csv`
- ✅ `cleaned_nirf_rankings.csv`

---

## 📊 What You'll See When Running

```
================================================================================
COLLEGE DATA CLEANING PROCESS
================================================================================

This script will clean and standardize all three datasets.
Cleaned files will be saved with 'cleaned_' prefix.

================================================================================
CLEANING: engineering colleges in India.csv
================================================================================
✓ Loaded 5447 rows

1. Standardizing college names...
   ✓ Cleaned 5447 college names

2. Handling missing values...
   ✓ Genders Accepted: 0 missing values handled
   ✓ City: 0 missing values handled
   ✓ State: 0 missing values handled
   ...

3. Cleaning course names...
   ✓ Cleaned course names (removed line breaks and standardized)

4. Normalizing fee structure...
   ✓ Normalized 4523 fee values
   ✓ Fee range: ₹25,473 to ₹2,009,710

5. Cleaning facilities data...
   ✓ Cleaned facilities information

✓ SAVED: data/cleaned_engineering_colleges_india.csv
  Rows: 5447, Columns: 15

[... continues for other datasets ...]

================================================================================
CLEANING COMPLETE!
================================================================================

📊 Summary:
  • cleaned_engineering_colleges_india.csv: 5447 rows
  • cleaned_engineering.csv: 5818 rows
  • cleaned_nirf_rankings.csv: 202 rows

  Total records processed: 11,467

✅ All datasets cleaned successfully!
```

---

## 🔧 Understanding the Code Structure

### **Helper Functions** (Reusable)
```python
standardize_college_name()  # Fixes college names
clean_course_name()         # Fixes course names
normalize_fee()             # Fixes fee values
handle_missing_values()     # Fills empty cells
```

### **Main Functions** (One per dataset)
```python
clean_engineering_colleges_india()  # Cleans dataset 1
clean_engineering_csv()             # Cleans dataset 2
clean_nirf_rankings()               # Cleans dataset 3
```

### **Execution**
```python
main()  # Runs all cleaning functions
```

---

## 🎓 Key Concepts Explained

### **Regular Expressions (regex)**
```python
re.sub(r'\s+', ' ', text)  # Replace multiple spaces with one
#      ^^^^                   Pattern to match
#             ^^^             Replacement
#                  ^^^^       Text to clean
```

### **Pandas DataFrames**
```python
df = pd.read_csv('file.csv')     # Load CSV into memory
df['column'].apply(function)      # Apply function to each cell
df.fillna('value')                # Fill empty cells
df.to_csv('output.csv')           # Save to new file
```

### **Error Handling**
```python
try:
    fee = float(fee_str)  # Try to convert to number
except:
    fee = np.nan          # If fails, set to "Not a Number"
```

---

## ✅ Benefits of Cleaning

| Before Cleaning | After Cleaning |
|----------------|----------------|
| "IIT  Madras\n" | "IIT Madras" |
| City: "" | City: "Not Available" |
| "CSE" | "Computer Science and Engineering" |
| "₹3,50,600" | 350600.0 |
| Inconsistent! ❌ | Consistent! ✅ |

---

## 🚀 Next Steps After Cleaning

1. ✅ **Review the cleaned files** - Open them in Excel/VS Code
2. ✅ **Verify the cleaning** - Check if names look good
3. ✅ **Data Merging** - Combine all three into one master dataset
4. ✅ **Database Import** - Load into PostgreSQL/SQLite

---

## 🆘 Common Issues & Solutions

### Issue: "File not found"
```
Solution: Make sure you're in the correct directory
cd C:\Users\mayus\Documents\GitHub\college-recommendation-system
```

### Issue: "pandas not found"
```
Solution: Install pandas
pip install pandas numpy
```

### Issue: Script runs but no output
```
Solution: Check if data folder exists and has the CSV files
```

---

## 📝 Summary

**What we're doing:**
1. Making college names consistent across all files
2. Replacing empty/missing values with "Not Available" or 0
3. Removing line breaks from course names
4. Converting fees to pure numbers (removing ₹, commas)

**Why it matters:**
- Makes data searchable
- Enables database storage
- Allows proper comparisons
- Powers the chatbot's recommendations

**Result:**
Clean, standardized data ready for your chatbot! 🎉
