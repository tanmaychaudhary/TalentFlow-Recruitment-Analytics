import psycopg2
from faker import Faker
import random
from datetime import timedelta

fake = Faker()

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="talentflow_db",
    user="postgres",
    password="9058",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Recruiters
for _ in range(5):
    cur.execute("""
        INSERT INTO recruiters (name, email)
        VALUES (%s, %s)
    """, (fake.name(), fake.email()))

# Job Postings
departments = ["Tech", "HR", "Marketing", "Finance"]
for _ in range(10):
    cur.execute("""
        INSERT INTO job_postings (title, department, location, status, posted_date)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        fake.job(),
        random.choice(departments),
        fake.city(),
        random.choice(["Open", "Closed"]),
        fake.date_between(start_date='-60d', end_date='today')
    ))

# Candidates
for _ in range(120):
    cur.execute("""
        INSERT INTO candidates (full_name, email, phone, education_level, experience_years, applied_date)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        fake.name(),
        fake.unique.email(),
        fake.phone_number()[:15],
        random.choice(["B.Tech", "MBA", "B.Sc", "M.Tech"]),
        round(random.uniform(0, 10), 1),
        fake.date_between(start_date='-30d', end_date='today')
    ))

# Fetch candidate & job IDs
cur.execute("SELECT candidate_id FROM candidates")
candidate_ids = [row[0] for row in cur.fetchall()]
cur.execute("SELECT job_id FROM job_postings")
job_ids = [row[0] for row in cur.fetchall()]

# Applications
application_statuses = ['Active', 'Rejected', 'Hired']
for _ in range(150):
    cid = random.choice(candidate_ids)
    jid = random.choice(job_ids)
    cur.execute("""
        INSERT INTO applications (candidate_id, job_id, application_date, current_stage, application_status)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        cid,
        jid,
        fake.date_between(start_date='-30d', end_date='today'),
        random.choice(['Applied', 'Screen', 'Interview', 'Offer', 'Final']),
        random.choices(application_statuses, weights=[0.6, 0.3, 0.1])[0]
    ))

# Interview Stages
cur.execute("SELECT application_id FROM applications")
app_ids = [row[0] for row in cur.fetchall()]
for _ in range(100):
    aid = random.choice(app_ids)
    cur.execute("""
        INSERT INTO interview_stages (application_id, stage_name, interviewer, stage_date, result)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        aid,
        random.choice(['Phone Screen', 'Technical Round', 'HR Round']),
        fake.name(),
        fake.date_between(start_date='-20d', end_date='today'),
        random.choice(['Passed', 'Failed', 'Pending'])
    ))

# Offers
for aid in random.sample(app_ids, 40):
    accepted = random.choice([True, False])
    cur.execute("""
        INSERT INTO offers (application_id, offer_date, offered_salary, accepted, decision_date)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        aid,
        fake.date_between(start_date='-15d', end_date='today'),
        round(random.uniform(50000, 120000), 2),
        accepted,
        fake.date_between(start_date='-10d', end_date='today') if accepted else None
    ))

# Hires
for aid in random.sample(app_ids, 20):
    cur.execute("""
        INSERT INTO hires (application_id, hire_date, onboarded)
        VALUES (%s, %s, %s)
    """, (
        aid,
        fake.date_between(start_date='-10d', end_date='today'),
        random.choice([True, False])
    ))

conn.commit()
cur.close()
conn.close()