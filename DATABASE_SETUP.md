# 🗄️ DATABASE SETUP GUIDE - PostgreSQL

## Phase 2: Database Setup - Step-by-Step Instructions

---

## 📋 Prerequisites

- ✅ PostgreSQL installed (you have pgAdmin 4)
- ✅ Enriched data files ready (`enriched_master_colleges.csv`, `enriched_master_courses.csv`)
- ✅ Python with `psycopg2` library

---

## 🚀 Step 1: Create Database in pgAdmin

### Option A: Using pgAdmin GUI

1. **Open pgAdmin 4**
2. **Connect to PostgreSQL Server** (default: localhost)
3. **Right-click on "Databases"** → Select **"Create" → "Database..."**
4. **Enter Database Details:**
   - Database name: `college_recommendation`
   - Owner: `postgres` (or your username)
   - Click **"Save"**

### Option B: Using SQL Query Tool

```sql
-- Open Query Tool in pgAdmin and run:
CREATE DATABASE college_recommendation
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;
```

---

## 🗂️ Step 2: Create Database Schema

1. **Open the database** `college_recommendation` in pgAdmin
2. **Right-click on the database** → Select **"Query Tool"**
3. **Open the file** `database_schema.sql` (created in project folder)
4. **Copy all contents** and paste into Query Tool
5. **Click "Execute" (F5)** to run the schema

**Or use this command:**

```powershell
# In PowerShell (from project directory):
psql -U postgres -d college_recommendation -f database_schema.sql
```

### ✅ Verify Schema Creation

Run this query in pgAdmin:

```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
ORDER BY table_name;
```

**Expected Output:** 4 tables
- `colleges`
- `college_facilities`
- `courses`
- `course_features`

---

## 📦 Step 3: Install Python Dependencies

```powershell
# Install PostgreSQL adapter for Python
pip install psycopg2

# Or if you get errors, try the binary version:
pip install psycopg2-binary
```

---

## ⚙️ Step 4: Configure Database Connection

1. **Open** `database_import.py`
2. **Update the DB_CONFIG section** (around line 16):

```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'college_recommendation',
    'user': 'postgres',  # Your PostgreSQL username
    'password': 'YOUR_PASSWORD_HERE'  # Your PostgreSQL password
}
```

**⚠️ Important:** Replace `YOUR_PASSWORD_HERE` with your actual PostgreSQL password!

---

## 🚀 Step 5: Import Data into Database

Run the import script:

```powershell
python database_import.py
```

### Expected Output:

```
============================================================
COLLEGE RECOMMENDATION SYSTEM - DATABASE IMPORT
============================================================
✅ Successfully connected to PostgreSQL database!
✅ All required tables found: colleges, courses, college_facilities, course_features

📂 Loading CSV files...
✅ Loaded 5,515 colleges
✅ Loaded 2,786 courses

📥 Importing colleges...
   Imported 500 colleges...
   Imported 1000 colleges...
   ...
✅ Successfully imported 5,515 colleges

📥 Importing college facilities...
   Imported 500 facility records...
   ...
✅ Successfully imported 5,515 facility records

📥 Importing courses...
   Imported 500 courses...
   ...
✅ Successfully imported 2,786 courses

🔍 Verifying imported data...

📊 Import Summary:
   Colleges: 5,515
   Facilities: 5,515
   Courses: 2,786

🔍 Sample Queries:

   Top 5 Colleges by Overall Score:
      IIT Madras - Indian Institute of Technology | Tier: Premium | Score: 91.35 | NIRF: 1
      ...

   CS-Related Courses: 674
   Colleges with Hostel: 4,447

✅ Database import completed successfully!
```

---

## 🔍 Step 6: Verify Data in pgAdmin

### Query 1: Check College Count

```sql
SELECT COUNT(*) AS total_colleges FROM colleges;
-- Expected: 5,515
```

### Query 2: View Top 10 Colleges

```sql
SELECT 
    college_name, 
    state, 
    tier, 
    nirf_rank, 
    overall_score 
FROM colleges 
ORDER BY overall_score DESC 
LIMIT 10;
```

### Query 3: Check Facilities

```sql
SELECT 
    c.college_name,
    f.has_hostel,
    f.has_library,
    f.has_gym,
    f.has_sports
FROM colleges c
INNER JOIN college_facilities f ON c.college_id = f.college_id
LIMIT 10;
```

### Query 4: CS Courses with College Info

```sql
SELECT 
    c.college_name,
    co.course_name,
    co.fee_per_year,
    co.course_category
FROM courses co
INNER JOIN colleges c ON co.college_id = c.college_id
WHERE co.is_cs_related = TRUE
ORDER BY co.fee_per_year ASC
LIMIT 10;
```

---

## 📊 Database Schema Overview

### Table Structure:

```
colleges (5,515 rows)
├── college_id (PK)
├── college_name, state, city
├── nirf_rank, naac_grade, naac_score
├── tier (Premium/Mid-Tier/Budget/Entry)
├── affordability_score, facility_score, quality_score, overall_score
└── website

college_facilities (5,515 rows)
├── facility_id (PK)
├── college_id (FK → colleges)
├── has_hostel, has_library, has_sports, has_gym...
└── facilities_text

courses (2,786 rows)
├── course_id (PK)
├── college_id (FK → colleges)
├── course_name, degree_type, duration_years
├── total_fee, fee_per_year
├── course_category
└── is_cs_related, is_ai_ml, is_electronics...

course_features (future use)
├── feature_id (PK)
├── course_id (FK → courses)
└── exam_accepted, cutoff_rank, placement_info...
```

---

## 🎯 Useful Views Created

### 1. `vw_colleges_complete` - Complete college info with facilities

```sql
SELECT * FROM vw_colleges_complete 
WHERE state = 'Karnataka' AND has_hostel = TRUE 
LIMIT 10;
```

### 2. `vw_courses_with_colleges` - Courses with college details

```sql
SELECT * FROM vw_courses_with_colleges 
WHERE is_ai_ml = TRUE AND fee_per_year <= 200000 
ORDER BY overall_score DESC;
```

### 3. `vw_top_colleges` - Top 100 NIRF ranked colleges

```sql
SELECT * FROM vw_top_colleges;
```

---

## 🔧 Troubleshooting

### Issue 1: "Connection refused"
```
✅ Solution: 
- Make sure PostgreSQL service is running
- Check if port 5432 is correct
- Verify firewall settings
```

### Issue 2: "Authentication failed"
```
✅ Solution:
- Update DB_CONFIG with correct password
- Check pg_hba.conf for authentication method
- Use 'trust' or 'md5' method for localhost
```

### Issue 3: "Table already exists"
```
✅ Solution:
- The schema file has DROP TABLE statements at top
- Or manually drop tables in pgAdmin and re-run schema
```

### Issue 4: "psycopg2 installation error"
```
✅ Solution:
pip install psycopg2-binary
```

---

## 📈 Performance Optimization

The schema includes these indexes for fast queries:

- **College searches:** Name, state, city, tier
- **Rankings:** NIRF rank, overall score
- **Course searches:** Category, fees, degree type
- **Full-text search:** College and course names
- **Facility filters:** Individual facility flags

---

## 🎯 Next Steps

After successful database setup:

1. ✅ **Phase 2.1 Complete:** Database schema created
2. ✅ **Phase 2.2 Complete:** Data imported and verified
3. 🔄 **Next:** Phase 2.3 - Build FastAPI Backend
4. 🔄 **Next:** Phase 2.4 - Create API Endpoints

---

## 🚀 Quick Test Queries

```sql
-- 1. Top ranked colleges
SELECT college_name, nirf_rank, overall_score 
FROM colleges 
WHERE nirf_rank IS NOT NULL 
ORDER BY nirf_rank LIMIT 20;

-- 2. Budget-friendly CS courses
SELECT c.college_name, co.course_name, co.fee_per_year
FROM courses co
JOIN colleges c ON co.college_id = c.college_id
WHERE co.is_cs_related = TRUE AND co.fee_per_year <= 150000
ORDER BY co.fee_per_year;

-- 3. Colleges by state with facility count
SELECT 
    state,
    COUNT(*) as total_colleges,
    SUM(CASE WHEN f.has_hostel THEN 1 ELSE 0 END) as with_hostel
FROM colleges c
LEFT JOIN college_facilities f ON c.college_id = f.college_id
GROUP BY state
ORDER BY total_colleges DESC;

-- 4. Course category distribution
SELECT 
    course_category,
    COUNT(*) as course_count,
    AVG(fee_per_year) as avg_fee
FROM courses
WHERE course_category IS NOT NULL
GROUP BY course_category
ORDER BY course_count DESC;
```

---

## ✅ Checklist

- [ ] PostgreSQL installed and running
- [ ] Database `college_recommendation` created
- [ ] Schema executed (4 tables + 3 views created)
- [ ] psycopg2 installed
- [ ] DB_CONFIG updated with credentials
- [ ] database_import.py executed successfully
- [ ] Data verified (5,515 colleges, 2,786 courses)
- [ ] Sample queries tested in pgAdmin

---

**🎉 Once all checkboxes are complete, you're ready for Phase 2.3: Backend API Development!**
