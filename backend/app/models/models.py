"""
SQLAlchemy models for database tables.
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from app.core.database import Base


class College(Base):
    """College table model."""
    __tablename__ = "colleges"
    
    college_id = Column(Integer, primary_key=True, index=True)
    college_name = Column(String(500), nullable=False)
    state = Column(String(100), nullable=False, index=True)
    city = Column(String(100), nullable=False, index=True)
    ownership = Column(String(50))
    college_type = Column(String(100))
    nirf_rank = Column(Integer, index=True)
    naac_grade = Column(String(10))
    naac_score = Column(Float)
    tier = Column(String(20), index=True)
    affordability_score = Column(Float)
    facility_score = Column(Float)
    quality_score = Column(Float)
    overall_score = Column(Float, index=True)
    website = Column(Text)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    
    # Relationships
    facilities = relationship("CollegeFacility", back_populates="college", uselist=False, lazy="joined")
    courses = relationship("Course", back_populates="college", lazy="select")


class CollegeFacility(Base):
    """College facilities table model."""
    __tablename__ = "college_facilities"
    
    facility_id = Column(Integer, primary_key=True, index=True)
    college_id = Column(Integer, ForeignKey("colleges.college_id"), unique=True)
    has_hostel = Column(Boolean, default=False)
    has_library = Column(Boolean, default=False)
    has_sports = Column(Boolean, default=False)
    has_gym = Column(Boolean, default=False)
    has_cafeteria = Column(Boolean, default=False)
    has_medical = Column(Boolean, default=False)
    has_wifi = Column(Boolean, default=False)
    has_lab = Column(Boolean, default=False)
    has_auditorium = Column(Boolean, default=False)
    has_transport = Column(Boolean, default=False)
    facilities_text = Column(Text)
    created_at = Column(TIMESTAMP)
    
    # Relationships
    college = relationship("College", back_populates="facilities")


class Course(Base):
    """Courses table model."""
    __tablename__ = "courses"
    
    course_id = Column(Integer, primary_key=True, index=True)
    college_id = Column(Integer, ForeignKey("colleges.college_id"))
    course_name = Column(String(500), nullable=False)
    degree_type = Column(String(50))
    duration_years = Column(Integer)
    fee_per_year = Column(Float)
    total_fee = Column(Float)
    course_category = Column(String(100), index=True)
    is_cs_related = Column(Boolean, default=False)
    is_electronics = Column(Boolean, default=False)
    is_mechanical = Column(Boolean, default=False)
    is_civil = Column(Boolean, default=False)
    is_chemical = Column(Boolean, default=False)
    is_aerospace = Column(Boolean, default=False)
    is_ai_ml = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    
    # Relationships
    college = relationship("College", back_populates="courses")


class CourseFeature(Base):
    """Course features table model."""
    __tablename__ = "course_features"
    
    feature_id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.course_id"))
    specialization = Column(String(200))
    accreditation = Column(String(200))
    placement_rate = Column(Float)
    avg_salary = Column(Float)
    top_recruiters = Column(Text)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
