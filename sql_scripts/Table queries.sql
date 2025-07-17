-- 1. JOB POSTINGS
CREATE TABLE job_postings (
    job_id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    department VARCHAR(50),
    location VARCHAR(50),
    status VARCHAR(20) CHECK (status IN ('Open', 'Closed')),
    posted_date DATE
);

-- 2. CANDIDATES
CREATE TABLE candidates (
    candidate_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    education_level VARCHAR(50),
    experience_years NUMERIC(3,1),
    applied_date DATE
);

-- 3. APPLICATIONS
CREATE TABLE applications (
    application_id SERIAL PRIMARY KEY,
    candidate_id INT REFERENCES candidates(candidate_id),
    job_id INT REFERENCES job_postings(job_id),
    application_date DATE,
    current_stage VARCHAR(50),
    application_status VARCHAR(20) CHECK (application_status IN ('Active', 'Rejected', 'Hired'))
);

-- 4. INTERVIEW STAGES
CREATE TABLE interview_stages (
    stage_id SERIAL PRIMARY KEY,
    application_id INT REFERENCES applications(application_id),
    stage_name VARCHAR(50), -- Phone Screen, Tech Interview, etc.
    interviewer VARCHAR(100),
    stage_date DATE,
    result VARCHAR(20) CHECK (result IN ('Passed', 'Failed', 'Pending'))
);

-- 5. OFFERS
CREATE TABLE offers (
    offer_id SERIAL PRIMARY KEY,
    application_id INT REFERENCES applications(application_id),
    offer_date DATE,
    offered_salary NUMERIC(10,2),
    accepted BOOLEAN,
    decision_date DATE
);

-- 6. HIRES
CREATE TABLE hires (
    hire_id SERIAL PRIMARY KEY,
    application_id INT REFERENCES applications(application_id),
    hire_date DATE,
    onboarded BOOLEAN
);

-- 7. RECRUITERS
CREATE TABLE recruiters (
    recruiter_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE
);

-- 8. JOB - RECRUITER MAPPING (Many-to-Many)
CREATE TABLE job_recruiters (
    job_id INT REFERENCES job_postings(job_id),
    recruiter_id INT REFERENCES recruiters(recruiter_id),
    PRIMARY KEY (job_id, recruiter_id)
);


