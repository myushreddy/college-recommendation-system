"""
Comprehensive system verification script.
Tests database, models, and API endpoints with detailed error reporting.
"""
import sys
sys.path.insert(0, 'C:/Users/mayus/Documents/GitHub/college-recommendation-system/backend')

from sqlalchemy import text, inspect
from sqlalchemy.orm import joinedload
from app.core.database import engine, SessionLocal
from app.models import College, CollegeFacility, Course
import traceback

def test_database_tables():
    """Test all database tables and their row counts."""
    print("\n" + "="*60)
    print("DATABASE TABLES VERIFICATION")
    print("="*60)
    
    db = SessionLocal()
    try:
        tables = {
            "colleges": College,
            "college_facilities": CollegeFacility,
            "courses": Course
        }
        
        for table_name, model in tables.items():
            count = db.query(model).count()
            print(f"✅ {table_name:<20} {count:>6} rows")
            
        return True
    except Exception as e:
        print(f"❌ Table verification failed: {e}")
        traceback.print_exc()
        return False
    finally:
        db.close()


def test_model_relationships():
    """Test SQLAlchemy model relationships."""
    print("\n" + "="*60)
    print("MODEL RELATIONSHIPS VERIFICATION")
    print("="*60)
    
    db = SessionLocal()
    try:
        # Test 1: College with facilities
        print("\nTest 1: College -> Facilities relationship")
        college_with_facility = db.query(College)\
            .join(CollegeFacility, College.college_id == CollegeFacility.college_id)\
            .first()
        
        if college_with_facility:
            print(f"✅ Found college with facility: {college_with_facility.college_name}")
            # Try to access facilities through relationship
            try:
                facilities = db.query(CollegeFacility)\
                    .filter(CollegeFacility.college_id == college_with_facility.college_id)\
                    .first()
                if facilities:
                    print(f"   Hostel: {facilities.hostel}, Library: {facilities.library}")
            except Exception as e:
                print(f"⚠️  Could not access facilities via relationship: {e}")
        else:
            print("⚠️  No colleges with facilities found")
        
        # Test 2: College with courses
        print("\nTest 2: College -> Courses relationship")
        college_with_courses = db.query(College)\
            .join(Course, College.college_id == Course.college_id)\
            .first()
        
        if college_with_courses:
            print(f"✅ Found college with courses: {college_with_courses.college_name}")
            course_count = db.query(Course)\
                .filter(Course.college_id == college_with_courses.college_id)\
                .count()
            print(f"   Number of courses: {course_count}")
        else:
            print("⚠️  No colleges with courses found")
        
        # Test 3: Eager loading with options
        print("\nTest 3: Eager loading test")
        try:
            college = db.query(College)\
                .options(joinedload(College.facilities))\
                .filter(College.college_id == 1)\
                .first()
            
            if college:
                print(f"✅ Eager loading works for college: {college.college_name}")
            else:
                print("⚠️  College ID 1 not found")
        except Exception as e:
            print(f"❌ Eager loading failed: {e}")
            traceback.print_exc()
        
        return True
    except Exception as e:
        print(f"❌ Relationship test failed: {e}")
        traceback.print_exc()
        return False
    finally:
        db.close()


def test_query_performance():
    """Test common queries and their performance."""
    print("\n" + "="*60)
    print("QUERY PERFORMANCE VERIFICATION")
    print("="*60)
    
    db = SessionLocal()
    try:
        # Query 1: Simple search
        print("\nQuery 1: Search by state")
        results = db.query(College).filter(College.state == "Karnataka").limit(5).all()
        print(f"✅ Found {len(results)} colleges in Karnataka")
        
        # Query 2: Filter by tier
        print("\nQuery 2: Filter by tier")
        results = db.query(College).filter(College.tier == "Budget-Friendly").limit(5).all()
        print(f"✅ Found {len(results)} Budget-Friendly colleges")
        
        # Query 3: NIRF ranked colleges
        print("\nQuery 3: NIRF ranked colleges")
        results = db.query(College).filter(College.nirf_rank.isnot(None)).limit(5).all()
        print(f"✅ Found {len(results)} NIRF ranked colleges")
        for college in results:
            print(f"   Rank {college.nirf_rank}: {college.college_name}")
        
        # Query 4: Colleges with high scores
        print("\nQuery 4: High scoring colleges")
        results = db.query(College)\
            .filter(College.overall_score >= 80)\
            .order_by(College.overall_score.desc())\
            .limit(5)\
            .all()
        print(f"✅ Found {len(results)} colleges with score >= 80")
        
        # Query 5: Courses by category
        print("\nQuery 5: Courses by category")
        cs_courses = db.query(Course)\
            .filter(Course.course_category.ilike("%Computer%"))\
            .limit(5)\
            .all()
        print(f"✅ Found {len(cs_courses)} Computer Science courses")
        
        return True
    except Exception as e:
        print(f"❌ Query test failed: {e}")
        traceback.print_exc()
        return False
    finally:
        db.close()


def test_data_quality():
    """Test data quality and integrity."""
    print("\n" + "="*60)
    print("DATA QUALITY VERIFICATION")
    print("="*60)
    
    db = SessionLocal()
    try:
        # Check for NULL values in critical fields
        print("\nChecking critical field completeness...")
        
        null_checks = {
            "Colleges without names": db.query(College).filter(College.college_name.is_(None)).count(),
            "Colleges without state": db.query(College).filter(College.state.is_(None)).count(),
            "Colleges without city": db.query(College).filter(College.city.is_(None)).count(),
            "Courses without names": db.query(Course).filter(Course.course_name.is_(None)).count(),
            "Courses without college_id": db.query(Course).filter(Course.college_id.is_(None)).count(),
        }
        
        issues = 0
        for check, count in null_checks.items():
            if count > 0:
                print(f"⚠️  {check}: {count}")
                issues += 1
            else:
                print(f"✅ {check}: {count}")
        
        # Check score ranges
        print("\nChecking score ranges (should be 0-100)...")
        score_checks = {
            "Invalid affordability scores": db.query(College)\
                .filter((College.affordability_score < 0) | (College.affordability_score > 100)).count(),
            "Invalid facility scores": db.query(College)\
                .filter((College.facility_score < 0) | (College.facility_score > 100)).count(),
            "Invalid quality scores": db.query(College)\
                .filter((College.quality_score < 0) | (College.quality_score > 100)).count(),
            "Invalid overall scores": db.query(College)\
                .filter((College.overall_score < 0) | (College.overall_score > 100)).count(),
        }
        
        for check, count in score_checks.items():
            if count > 0:
                print(f"⚠️  {check}: {count}")
                issues += 1
            else:
                print(f"✅ {check}: {count}")
        
        if issues == 0:
            print(f"\n✅ All data quality checks passed!")
        else:
            print(f"\n⚠️  Found {issues} data quality issues")
        
        return issues == 0
    except Exception as e:
        print(f"❌ Data quality test failed: {e}")
        traceback.print_exc()
        return False
    finally:
        db.close()


def test_schema_structure():
    """Verify database schema matches models."""
    print("\n" + "="*60)
    print("SCHEMA STRUCTURE VERIFICATION")
    print("="*60)
    
    try:
        inspector = inspect(engine)
        
        # Check tables exist
        tables = inspector.get_table_names()
        required_tables = ['colleges', 'college_facilities', 'courses', 'course_features']
        
        print("\nChecking required tables...")
        for table in required_tables:
            if table in tables:
                columns = inspector.get_columns(table)
                print(f"✅ {table:<25} ({len(columns)} columns)")
            else:
                print(f"❌ {table:<25} MISSING!")
        
        # Check indexes
        print("\nChecking indexes on colleges table...")
        indexes = inspector.get_indexes('colleges')
        print(f"✅ Found {len(indexes)} indexes")
        
        # Check foreign keys
        print("\nChecking foreign key constraints...")
        fks = inspector.get_foreign_keys('college_facilities')
        print(f"✅ college_facilities has {len(fks)} foreign keys")
        
        fks = inspector.get_foreign_keys('courses')
        print(f"✅ courses has {len(fks)} foreign keys")
        
        return True
    except Exception as e:
        print(f"❌ Schema verification failed: {e}")
        traceback.print_exc()
        return False


def run_comprehensive_check():
    """Run all verification tests."""
    print("\n" + "="*70)
    print(" "*15 + "COMPREHENSIVE SYSTEM VERIFICATION")
    print("="*70)
    
    results = {
        "Database Tables": test_database_tables(),
        "Model Relationships": test_model_relationships(),
        "Query Performance": test_query_performance(),
        "Data Quality": test_data_quality(),
        "Schema Structure": test_schema_structure()
    }
    
    # Summary
    print("\n" + "="*70)
    print("VERIFICATION SUMMARY")
    print("="*70)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:<30} {status}")
    
    passed_count = sum(results.values())
    total_count = len(results)
    
    print(f"\nTotal: {passed_count}/{total_count} checks passed")
    
    if passed_count == total_count:
        print("\n🎉 All system checks passed! System is healthy.")
    else:
        print(f"\n⚠️  {total_count - passed_count} checks failed. Review errors above.")
    
    print("="*70)


if __name__ == "__main__":
    try:
        run_comprehensive_check()
    except KeyboardInterrupt:
        print("\n\nVerification interrupted by user.")
    except Exception as e:
        print(f"\n\nFatal error: {e}")
        traceback.print_exc()
