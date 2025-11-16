"""
Check actual database schema to see column names.
"""
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="college_recommendation",
    user="postgres",
    password="Ayush@123"
)

cur = conn.cursor()

# Check college_facilities columns
print("="*60)
print("COLLEGE_FACILITIES TABLE COLUMNS:")
print("="*60)
cur.execute("""
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_name = 'college_facilities'
    ORDER BY ordinal_position
""")
for row in cur.fetchall():
    print(f"  {row[0]:<30} {row[1]}")

# Check courses columns
print("\n" + "="*60)
print("COURSES TABLE COLUMNS:")
print("="*60)
cur.execute("""
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_name = 'courses'
    ORDER BY ordinal_position
""")
for row in cur.fetchall():
    print(f"  {row[0]:<30} {row[1]}")

# Check colleges columns
print("\n" + "="*60)
print("COLLEGES TABLE COLUMNS:")
print("="*60)
cur.execute("""
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_name = 'colleges'
    ORDER BY ordinal_position
""")
for row in cur.fetchall():
    print(f"  {row[0]:<30} {row[1]}")

cur.close()
conn.close()
