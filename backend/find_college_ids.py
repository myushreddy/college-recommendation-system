"""
Find valid college IDs.
"""
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="college_recommendation",
    user="postgres",
    password="Ayush@123"
)

cur = conn.cursor()
cur.execute("SELECT college_id, college_name FROM colleges ORDER BY college_id LIMIT 10")
print("First 10 colleges in database:")
print("="*60)
for college_id, name in cur.fetchall():
    print(f"ID: {college_id:>6}  {name}")

cur.close()
conn.close()
