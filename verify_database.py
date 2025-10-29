"""
Run verification queries on the college recommendation database
"""
import psycopg2

# Database config
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'college_recommendation',
    'user': 'postgres',
    'password': 'Ayush@123'
}

def run_query(cur, title, query):
    """Run a query and display results"""
    print("\n" + "=" * 100)
    print(title)
    print("=" * 100)
    cur.execute(query)
    results = cur.fetchall()
    
    if results:
        # Get column names
        colnames = [desc[0] for desc in cur.description]
        
        # Print header
        header = " | ".join(f"{col:20s}" for col in colnames)
        print(header)
        print("-" * len(header))
        
        # Print rows
        for row in results:
            formatted_row = []
            for val in row:
                if val is None:
                    formatted_row.append("N/A".ljust(20))
                elif isinstance(val, float):
                    formatted_row.append(f"{val:.2f}".ljust(20))
                elif isinstance(val, int):
                    formatted_row.append(str(val).ljust(20))
                else:
                    formatted_row.append(str(val)[:20].ljust(20))
            print(" | ".join(formatted_row))
        
        print(f"\n({len(results)} rows)")
    else:
        print("No results found.")

# Connect to database
print("Connecting to database...")
conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

# Query 1: Check counts
run_query(cur, 
    "QUERY 1: Total Counts",
    """
    SELECT 
        (SELECT COUNT(*) FROM colleges) as colleges,
        (SELECT COUNT(*) FROM courses) as courses,
        (SELECT COUNT(*) FROM college_facilities) as facilities
    """
)

# Query 2: Top 10 colleges by overall score
run_query(cur,
    "QUERY 2: Top 10 Colleges by Overall Score",
    """
    SELECT 
        college_name, 
        state,
        tier, 
        overall_score, 
        nirf_rank 
    FROM colleges 
    ORDER BY overall_score DESC NULLS LAST 
    LIMIT 10
    """
)

# Query 3: Top 10 NIRF ranked colleges
run_query(cur,
    "QUERY 3: Top 10 NIRF Ranked Colleges",
    """
    SELECT 
        nirf_rank,
        college_name, 
        state,
        overall_score,
        tier
    FROM colleges 
    WHERE nirf_rank IS NOT NULL
    ORDER BY nirf_rank
    LIMIT 10
    """
)

# Query 4: Colleges with CS courses
run_query(cur,
    "QUERY 4: Colleges with CS-Related Courses",
    """
    SELECT 
        c.college_name, 
        c.state,
        co.course_name, 
        co.course_category,
        co.fee_per_year
    FROM colleges c
    JOIN courses co ON c.college_id = co.college_id
    WHERE co.is_cs_related = TRUE
    ORDER BY c.nirf_rank NULLS LAST
    LIMIT 10
    """
)

# Query 5: Colleges with facilities
run_query(cur,
    "QUERY 5: Top Colleges with Best Facilities",
    """
    SELECT 
        c.college_name,
        c.state,
        c.facility_score,
        f.has_hostel,
        f.has_library,
        f.has_gym,
        f.has_sports
    FROM colleges c
    JOIN college_facilities f ON c.college_id = f.college_id
    WHERE c.facility_score IS NOT NULL
    ORDER BY c.facility_score DESC
    LIMIT 10
    """
)

# Query 6: Budget-friendly colleges
run_query(cur,
    "QUERY 6: Budget-Friendly Colleges (High Affordability Score)",
    """
    SELECT 
        college_name,
        state,
        tier,
        affordability_score,
        overall_score
    FROM colleges
    WHERE affordability_score IS NOT NULL
    ORDER BY affordability_score DESC
    LIMIT 10
    """
)

# Query 7: State-wise college distribution
run_query(cur,
    "QUERY 7: State-wise College Distribution",
    """
    SELECT 
        state,
        COUNT(*) as total_colleges,
        COUNT(CASE WHEN nirf_rank IS NOT NULL THEN 1 END) as nirf_ranked,
        ROUND(AVG(overall_score), 2) as avg_score
    FROM colleges
    WHERE state IS NOT NULL
    GROUP BY state
    ORDER BY total_colleges DESC
    LIMIT 15
    """
)

# Query 8: Course category distribution
run_query(cur,
    "QUERY 8: Course Category Distribution",
    """
    SELECT 
        course_category,
        COUNT(*) as total_courses,
        COUNT(DISTINCT college_id) as colleges_offering,
        ROUND(AVG(fee_per_year), 2) as avg_fee
    FROM courses
    WHERE course_category IS NOT NULL
    GROUP BY course_category
    ORDER BY total_courses DESC
    """
)

cur.close()
conn.close()

print("\n" + "=" * 80)
print("✅ All queries completed successfully!")
print("=" * 80)
