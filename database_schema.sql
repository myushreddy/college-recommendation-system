-- ============================================
-- COLLEGE RECOMMENDATION SYSTEM - DATABASE SCHEMA
-- PostgreSQL Database Setup
-- ============================================

-- Drop existing tables if they exist (careful in production!)
DROP TABLE IF EXISTS course_features CASCADE;
DROP TABLE IF EXISTS courses CASCADE;
DROP TABLE IF EXISTS college_facilities CASCADE;
DROP TABLE IF EXISTS colleges CASCADE;

-- ============================================
-- TABLE 1: COLLEGES (Main college information)
-- ============================================
CREATE TABLE colleges (
    -- Primary Key
    college_id SERIAL PRIMARY KEY,
    
    -- Basic Information
    college_name VARCHAR(500) NOT NULL,
    state VARCHAR(100),
    city VARCHAR(100),
    ownership VARCHAR(50), -- Government/Private/Autonomous
    college_type VARCHAR(100),
    
    -- Rankings & Recognition
    nirf_rank INTEGER,
    naac_grade VARCHAR(10),
    naac_score DECIMAL(4,2),
    
    -- Tier Classification
    tier VARCHAR(20), -- Premium/Mid-Tier/Budget-Friendly/Entry-Level
    
    -- Scores (0-100 scale)
    affordability_score DECIMAL(5,2),
    facility_score DECIMAL(5,2),
    quality_score DECIMAL(5,2),
    overall_score DECIMAL(5,2),
    
    -- Contact & Location
    website VARCHAR(500),
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes for fast searching
    CONSTRAINT unique_college_name UNIQUE(college_name, state, city)
);

-- Create indexes for fast queries
CREATE INDEX idx_colleges_state ON colleges(state);
CREATE INDEX idx_colleges_city ON colleges(city);
CREATE INDEX idx_colleges_tier ON colleges(tier);
CREATE INDEX idx_colleges_nirf_rank ON colleges(nirf_rank);
CREATE INDEX idx_colleges_overall_score ON colleges(overall_score DESC);
CREATE INDEX idx_colleges_affordability ON colleges(affordability_score DESC);
CREATE INDEX idx_colleges_name_search ON colleges USING gin(to_tsvector('english', college_name));


-- ============================================
-- TABLE 2: COLLEGE_FACILITIES (Facility flags)
-- ============================================
CREATE TABLE college_facilities (
    facility_id SERIAL PRIMARY KEY,
    college_id INTEGER NOT NULL REFERENCES colleges(college_id) ON DELETE CASCADE,
    
    -- Facility Flags (Boolean)
    has_hostel BOOLEAN DEFAULT FALSE,
    has_library BOOLEAN DEFAULT FALSE,
    has_sports BOOLEAN DEFAULT FALSE,
    has_gym BOOLEAN DEFAULT FALSE,
    has_cafeteria BOOLEAN DEFAULT FALSE,
    has_medical BOOLEAN DEFAULT FALSE,
    has_wifi BOOLEAN DEFAULT FALSE,
    has_lab BOOLEAN DEFAULT FALSE,
    has_auditorium BOOLEAN DEFAULT FALSE,
    has_transport BOOLEAN DEFAULT FALSE,
    
    -- Raw facilities text (for reference)
    facilities_text TEXT,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT unique_college_facility UNIQUE(college_id)
);

CREATE INDEX idx_facilities_college ON college_facilities(college_id);
CREATE INDEX idx_facilities_hostel ON college_facilities(has_hostel) WHERE has_hostel = TRUE;
CREATE INDEX idx_facilities_sports ON college_facilities(has_sports) WHERE has_sports = TRUE;


-- ============================================
-- TABLE 3: COURSES (Course offerings)
-- ============================================
CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    college_id INTEGER NOT NULL REFERENCES colleges(college_id) ON DELETE CASCADE,
    
    -- Course Information
    course_name VARCHAR(500) NOT NULL,
    degree_type VARCHAR(50), -- B.Tech/M.Tech/MBA/etc
    duration_years INTEGER,
    
    -- Fees
    total_fee DECIMAL(12,2),
    fee_per_year DECIMAL(12,2),
    
    -- Course Category
    course_category VARCHAR(100), -- CS, Electronics, Mechanical, etc.
    
    -- Specializations (if applicable)
    is_cs_related BOOLEAN DEFAULT FALSE,
    is_ai_ml BOOLEAN DEFAULT FALSE,
    is_electronics BOOLEAN DEFAULT FALSE,
    is_mechanical BOOLEAN DEFAULT FALSE,
    is_civil BOOLEAN DEFAULT FALSE,
    is_chemical BOOLEAN DEFAULT FALSE,
    is_aerospace BOOLEAN DEFAULT FALSE,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for course queries
CREATE INDEX idx_courses_college ON courses(college_id);
CREATE INDEX idx_courses_category ON courses(course_category);
CREATE INDEX idx_courses_degree ON courses(degree_type);
CREATE INDEX idx_courses_fee ON courses(fee_per_year);
CREATE INDEX idx_courses_cs_related ON courses(is_cs_related) WHERE is_cs_related = TRUE;
CREATE INDEX idx_courses_ai_ml ON courses(is_ai_ml) WHERE is_ai_ml = TRUE;
CREATE INDEX idx_courses_name_search ON courses USING gin(to_tsvector('english', course_name));


-- ============================================
-- TABLE 4: COURSE_FEATURES (Additional course metadata)
-- ============================================
CREATE TABLE course_features (
    feature_id SERIAL PRIMARY KEY,
    course_id INTEGER NOT NULL REFERENCES courses(course_id) ON DELETE CASCADE,
    
    -- Admission Details
    exam_accepted VARCHAR(200), -- JEE Main, JEE Advanced, State CET, etc.
    cutoff_rank INTEGER,
    seats_available INTEGER,
    
    -- Placement Info (if available in future)
    avg_placement_package DECIMAL(12,2),
    highest_package DECIMAL(12,2),
    placement_percentage DECIMAL(5,2),
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT unique_course_feature UNIQUE(course_id)
);

CREATE INDEX idx_course_features_course ON course_features(course_id);


-- ============================================
-- VIEWS FOR COMMON QUERIES
-- ============================================

-- Complete college view with facilities
CREATE VIEW vw_colleges_complete AS
SELECT 
    c.college_id,
    c.college_name,
    c.state,
    c.city,
    c.ownership,
    c.college_type,
    c.nirf_rank,
    c.naac_grade,
    c.naac_score,
    c.tier,
    c.affordability_score,
    c.facility_score,
    c.quality_score,
    c.overall_score,
    c.website,
    f.has_hostel,
    f.has_library,
    f.has_sports,
    f.has_gym,
    f.has_cafeteria,
    f.has_medical,
    f.has_wifi,
    f.has_lab,
    f.has_auditorium,
    f.has_transport,
    f.facilities_text
FROM colleges c
LEFT JOIN college_facilities f ON c.college_id = f.college_id;

-- Course details with college info
CREATE VIEW vw_courses_with_colleges AS
SELECT 
    co.course_id,
    co.course_name,
    co.degree_type,
    co.duration_years,
    co.total_fee,
    co.fee_per_year,
    co.course_category,
    co.is_cs_related,
    co.is_ai_ml,
    co.is_electronics,
    co.is_mechanical,
    c.college_id,
    c.college_name,
    c.state,
    c.city,
    c.tier,
    c.nirf_rank,
    c.overall_score
FROM courses co
INNER JOIN colleges c ON co.college_id = c.college_id;

-- Top ranked colleges view
CREATE VIEW vw_top_colleges AS
SELECT 
    college_id,
    college_name,
    state,
    city,
    nirf_rank,
    tier,
    overall_score,
    affordability_score,
    facility_score
FROM colleges
WHERE nirf_rank IS NOT NULL
ORDER BY nirf_rank ASC
LIMIT 100;


-- ============================================
-- UTILITY FUNCTIONS
-- ============================================

-- Function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for auto-updating timestamps
CREATE TRIGGER update_colleges_updated_at BEFORE UPDATE ON colleges
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_courses_updated_at BEFORE UPDATE ON courses
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();


-- ============================================
-- COMMENTS FOR DOCUMENTATION
-- ============================================
COMMENT ON TABLE colleges IS 'Main college information with scores and rankings';
COMMENT ON TABLE college_facilities IS 'Boolean flags for college facilities';
COMMENT ON TABLE courses IS 'Course offerings with fees and categories';
COMMENT ON TABLE course_features IS 'Additional course metadata like placements and cutoffs';

COMMENT ON COLUMN colleges.tier IS 'College tier: Premium/Mid-Tier/Budget-Friendly/Entry-Level';
COMMENT ON COLUMN colleges.affordability_score IS 'Score 0-100, higher = more affordable';
COMMENT ON COLUMN colleges.facility_score IS 'Score 0-100 based on available facilities';
COMMENT ON COLUMN colleges.quality_score IS 'Score 0-100 based on NAAC and rankings';
COMMENT ON COLUMN colleges.overall_score IS 'Weighted average of all scores';

-- ============================================
-- SAMPLE QUERIES (FOR TESTING)
-- ============================================

-- Query 1: Find top 10 colleges by overall score
-- SELECT * FROM colleges ORDER BY overall_score DESC LIMIT 10;

-- Query 2: Find CS courses under 2 lakhs per year
-- SELECT * FROM vw_courses_with_colleges 
-- WHERE is_cs_related = TRUE AND fee_per_year <= 200000 
-- ORDER BY overall_score DESC;

-- Query 3: Find colleges with hostel and gym in Karnataka
-- SELECT c.* FROM colleges c
-- INNER JOIN college_facilities f ON c.college_id = f.college_id
-- WHERE c.state = 'Karnataka' AND f.has_hostel = TRUE AND f.has_gym = TRUE;

-- Query 4: Top NIRF ranked colleges with AI/ML courses
-- SELECT DISTINCT c.college_name, c.nirf_rank, co.course_name
-- FROM colleges c
-- INNER JOIN courses co ON c.college_id = co.college_id
-- WHERE c.nirf_rank <= 50 AND co.is_ai_ml = TRUE
-- ORDER BY c.nirf_rank;

-- ============================================
-- END OF SCHEMA
-- ============================================
