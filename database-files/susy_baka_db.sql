DROP DATABASE IF EXISTS project_susy_baka;
CREATE DATABASE project_susy_baka;
USE project_susy_baka;

CREATE TABLE IF NOT EXISTS user (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    role ENUM('Student', 'School_Admin', 'HR_Manager', 'Maintenance_Staff') NOT NULL,
    dob DATE,
    gender ENUM('Male', 'Female', 'Other')
);

-- Create school_admin table
CREATE TABLE IF NOT EXISTS school_admin (
    admin_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    hire_date DATE,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create grade_record table
CREATE TABLE IF NOT EXISTS grade_record (
    grade_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    course_name VARCHAR(100) NOT NULL,
    grade DECIMAL(3, 2) CHECK (grade >= 0.0 AND grade <= 4.0),
    recorded_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    recorded_by INT,
    FOREIGN KEY (recorded_by) REFERENCES school_admin(admin_id)
        ON DELETE SET NULL ON UPDATE CASCADE
);




-- Create co_op_record table
CREATE TABLE IF NOT EXISTS co_op_record (
    co_op_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    company_name VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    approved_by INT,
    FOREIGN KEY (approved_by) REFERENCES school_admin(admin_id)
        ON DELETE SET NULL ON UPDATE CASCADE
);



-- Create student table
CREATE TABLE IF NOT EXISTS student (
    user_id INT PRIMARY KEY UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Create application table
CREATE TABLE IF NOT EXISTS application (
    application_id INT PRIMARY KEY,
    user_id INT,
    position_id INT,
    sent_on DATE DEFAULT NULL,
    status ENUM('Pending', 'Accepted', 'Rejected') NOT NULL,
    FOREIGN KEY (user_id) REFERENCES student(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create resume table
CREATE TABLE IF NOT EXISTS resume (
    resume_id INT PRIMARY KEY,
    user_id INT,
    time_uploaded TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    doc_name VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES student(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create suggestion table
CREATE TABLE IF NOT EXISTS suggestion (
    suggestion_id INT PRIMARY KEY,
    resume_id INT,
    time_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    suggestion_text TEXT,
    FOREIGN KEY (resume_id) REFERENCES resume(resume_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create hr_manager table
CREATE TABLE IF NOT EXISTS hr_manager (
    hr_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    user_id INT NOT NULL UNIQUE,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);



-- Create internship_position table
CREATE TABLE IF NOT EXISTS internship_position (
    position_id INT AUTO_INCREMENT PRIMARY KEY,
    hr_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    requirements TEXT,
    status ENUM('Active', 'Inactive') NOT NULL,
    posted_date DATE NOT NULL,
    FOREIGN KEY (hr_id) REFERENCES hr_manager(hr_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create maintenance_staff table
CREATE TABLE IF NOT EXISTS maintenance_staff (
    staff_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create database_info table
CREATE TABLE IF NOT EXISTS database_info (
    database_id INT NOT NULL AUTO_INCREMENT,
    change_id INT NOT NULL,
    staff_id INT NOT NULL,
    name VARCHAR(100),
    version VARCHAR(20),
    type VARCHAR(50),
    last_update DATE,
    PRIMARY KEY (database_id, change_id), -- Composite primary key
    UNIQUE (database_id),
    UNIQUE (change_id),
    FOREIGN KEY (staff_id) REFERENCES maintenance_staff(staff_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create data_alteration_history table
CREATE TABLE IF NOT EXISTS data_alteration_history (
    alteration_type VARCHAR(100),
    alteration_date DATE,
    change_id INT NOT NULL,
    FOREIGN KEY (change_id) REFERENCES database_info(change_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create backup_history table
CREATE TABLE IF NOT EXISTS backup_history (
    type VARCHAR(50),
    backup_date DATE,
    backup_type VARCHAR(100),
    details VARCHAR(255),
    change_id INT NOT NULL,
    FOREIGN KEY (change_id) REFERENCES database_info(change_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create alert_history table
CREATE TABLE IF NOT EXISTS alert_history (
    metrics VARCHAR(255),
    alerts VARCHAR(255),
    severity VARCHAR(255),
    database_id INT NOT NULL,
    FOREIGN KEY (database_id) REFERENCES database_info(database_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create update_history table
CREATE TABLE IF NOT EXISTS update_history (
    update_type VARCHAR(100),
    update_date DATE,
    details VARCHAR(255),
    change_id INT NOT NULL,
    FOREIGN KEY (change_id) REFERENCES database_info(change_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create internship_analytics table
CREATE TABLE IF NOT EXISTS internship_analytics(
    position_id INT,
    num_internships INT,
    average_apps INT,
    database_id INT NOT NULL,
    FOREIGN KEY (database_id) REFERENCES database_info(database_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (position_id) REFERENCES internship_position(position_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

SHOW tables;

//////////////////////////////////////////////
/* 1. Student
User Stories:
- Upload and edit resumes.
- View application history.
- Update application status.
- Delete unnecessary resumes.


-- Insert a new resume record for the student
INSERT INTO resume (resume_id, user_id, time_uploaded, doc_name)
VALUES (3, 1, NOW(), 'alice_updated_resume.pdf');

-- Retrieve all applications submitted by the student
SELECT application_id, position_id, sent_on, status
FROM application
WHERE user_id = 1; -- Fetch all applications submitted by Alice

-- Update the application status for a specific application
UPDATE application
SET status = 'Accepted'
WHERE application_id = 1;

-- Delete the resume record added in this CRUD
DELETE FROM resume
WHERE resume_id = 3 AND user_id = 1; -- Delete Alice's updated resume added above

2. School Admin
User Stories:
- Manage student records.
- Update student academic grades.
- Delete invalid student records.
- Query student academic performance.


-- Add a new student record
INSERT INTO user (full_name, email, role, dob, gender)
VALUES ('Charlie Green', 'charlie.green@student.com', 'Student', '2002-03-25', 'Male');

-- Add a grade for the new student
INSERT INTO grade_record (student_id, course_name, grade, recorded_date)
VALUES (3, 'Biology', 3.7, NOW()); -- Record Biology grade for Charlie

-- Update the grade of a specific student
UPDATE grade_record
SET grade = 3.9
WHERE grade_id = 1; -- Update Alice's Mathematics grade

-- Delete the new student record added in this CRUD
DELETE FROM user
WHERE full_name = 'Charlie Green' AND role = 'Student'; -- Delete Charlie Green's user record

-- Query academic performance of a specific student
SELECT user.full_name, grade_record.course_name, grade_record.grade
FROM user
JOIN grade_record ON user.user_id = grade_record.student_id
WHERE user.user_id = 1; -- Query Alice's academic performance

3. HR Manager
User Stories:
- Post and edit internship positions.
- Delete inactive job postings.
- Query the number of applicants for each position.
- Automatically filter resumes.


-- Insert a new internship position
INSERT INTO internship_position (hr_id, title, description, requirements, status, posted_date)
VALUES (1, 'Data Analyst Intern', 'Analyze datasets and generate reports.', 'Python, SQL',
        'Active', NOW()); -- Add new position by Emily

-- Edit the description of an internship position
UPDATE internship_position
SET description = 'Build APIs and manage databases efficiently.'
WHERE position_id = 1; -- Update Backend Developer Intern description

-- Delete the new internship position added in this CRUD
DELETE FROM internship_position
WHERE title = 'Data Analyst Intern'; -- Remove the newly added Data Analyst Intern position

-- Query the number of applications submitted for each job position
SELECT position_id, COUNT(application_id) AS num_applications
FROM application
GROUP BY position_id;

-- Automatically filter resumes based on suggestions
SELECT resume.user_id, resume.doc_name
FROM resume
JOIN suggestion ON resume.resume_id = suggestion.resume_id
WHERE suggestion_text LIKE '%technical skills%';

4. Maintenance Staff
User Stories:
- Add data cleansing tasks.
- Remove expired backups.
- Monitor system performance.
- Add new databases.


-- Add a data cleansing task
INSERT INTO data_alteration_history (alteration_type, alteration_date, change_id)
VALUES ('Index Reorganization', NOW(), 1);

-- Remove expired backups
DELETE FROM backup_history
WHERE backup_date < '2023-10-01';

-- Monitor system performance for a specific database
SELECT metrics, alerts, severity
FROM alert_history
WHERE database_id = 1;

-- Add a new database managed by maintenance staff
INSERT INTO database_info (change_id, staff_id, name, version, type, last_update)
VALUES (3, 2, 'AnalyticsDB', '1.0', 'Relational', NOW());

-- Delete the new database added in this CRUD
DELETE FROM database_info
WHERE name = 'AnalyticsDB' AND version = '1.0';
*/

-- Base User Data (38 records - Strong Entity)
INSERT INTO user (full_name, email, role, dob, gender) VALUES
-- Students (20)
('Alice Johnson', 'alice.j@student.com', 'Student', '2001-05-15', 'Female'),
('Bob Smith', 'bob.s@student.com', 'Student', '2000-09-20', 'Male'),
('Charlie Brown', 'charlie.b@student.com', 'Student', '2001-03-10', 'Male'),
('Diana Prince', 'diana.p@student.com', 'Student', '2000-07-12', 'Female'),
('Edward Norton', 'edward.n@student.com', 'Student', '2001-11-30', 'Male'),
('Fiona Apple', 'fiona.a@student.com', 'Student', '2000-12-25', 'Female'),
('George Banks', 'george.b@student.com', 'Student', '2001-01-15', 'Male'),
('Helen Carter', 'helen.c@student.com', 'Student', '2000-06-18', 'Female'),
('Ian Malcolm', 'ian.m@student.com', 'Student', '2001-08-22', 'Male'),
('Julia Roberts', 'julia.r@student.com', 'Student', '2000-04-05', 'Female'),
('Kevin Hart', 'kevin.h@student.com', 'Student', '2001-09-28', 'Male'),
('Laura Palmer', 'laura.p@student.com', 'Student', '2000-08-14', 'Female'),
('Michael Jordan', 'michael.j@student.com', 'Student', '2001-02-17', 'Male'),
('Nancy Wheeler', 'nancy.w@student.com', 'Student', '2000-10-31', 'Female'),
('Oscar Isaac', 'oscar.i@student.com', 'Student', '2001-07-09', 'Male'),
('Penny Lane', 'penny.l@student.com', 'Student', '2000-11-11', 'Female'),
('Quincy Jones', 'quincy.j@student.com', 'Student', '2001-04-23', 'Male'),
('Rachel Green', 'rachel.g@student.com', 'Student', '2000-05-27', 'Female'),
('Steve Rogers', 'steve.r@student.com', 'Student', '2001-06-14', 'Male'),
('Tina Turner', 'tina.t@student.com', 'Student', '2000-03-08', 'Female'),

-- School Admins (8)
('William Smith', 'william.s@school.com', 'School_Admin', '1980-03-12', 'Male'),
('Emma Davis', 'emma.d@school.com', 'School_Admin', '1975-11-22', 'Female'),
('James Wilson', 'james.w@school.com', 'School_Admin', '1978-07-15', 'Male'),
('Sarah Johnson', 'sarah.j@school.com', 'School_Admin', '1982-09-30', 'Female'),
('Robert Brown', 'robert.b@school.com', 'School_Admin', '1977-05-20', 'Male'),
('Mary Williams', 'mary.w@school.com', 'School_Admin', '1981-12-05', 'Female'),
('David Miller', 'david.m@school.com', 'School_Admin', '1979-08-18', 'Male'),
('Patricia Davis', 'patricia.d@school.com', 'School_Admin', '1983-02-28', 'Female'),

-- HR Managers (5)
('John Anderson', 'john.a@hr.com', 'HR_Manager', '1985-06-18', 'Male'),
('Lisa Taylor', 'lisa.t@hr.com', 'HR_Manager', '1982-02-25', 'Female'),
('Mark Thompson', 'mark.t@hr.com', 'HR_Manager', '1984-10-12', 'Male'),
('Karen White', 'karen.w@hr.com', 'HR_Manager', '1983-04-15', 'Female'),
('Paul Martin', 'paul.m@hr.com', 'HR_Manager', '1981-09-08', 'Male'),

-- Maintenance Staff (5)
('Thomas Anderson', 'thomas.a@maintenance.com', 'Maintenance_Staff', '1978-08-01', 'Male'),
('Susan Clark', 'susan.c@maintenance.com', 'Maintenance_Staff', '1980-04-14', 'Female'),
('Richard Lee', 'richard.l@maintenance.com', 'Maintenance_Staff', '1979-11-27', 'Male'),
('Jennifer Hall', 'jennifer.h@maintenance.com', 'Maintenance_Staff', '1981-06-23', 'Female'),
('Daniel King', 'daniel.k@maintenance.com', 'Maintenance_Staff', '1977-12-09', 'Male');

-- Student Table (mapping from user table)
INSERT INTO student (user_id, full_name, email)
SELECT user_id, full_name, email
FROM user
WHERE role = 'Student';

-- School Admin Table (mapping from user table)
INSERT INTO school_admin (user_id, full_name, hire_date)
SELECT user_id, full_name, DATE_SUB(CURRENT_DATE, INTERVAL FLOOR(RAND() * 1825) DAY)
FROM user
WHERE role = 'School_Admin';

-- HR Manager Table (mapping from user table)
INSERT INTO hr_manager (user_id, full_name, email)
SELECT user_id, full_name, email
FROM user
WHERE role = 'HR_Manager';

-- Maintenance Staff Table (mapping from user table)
INSERT INTO maintenance_staff (user_id, full_name)
SELECT user_id, full_name
FROM user
WHERE role = 'Maintenance_Staff';

-- Internship Positions (30 records)
INSERT INTO internship_position (hr_id, title, description, requirements, status, posted_date) VALUES
(1, 'Software Developer Intern', 'Develop and maintain web applications', 'Java, Spring Boot, SQL', 'Active', '2023-09-01'),
(2, 'Frontend Developer Intern', 'Create responsive user interfaces', 'React, TypeScript, CSS', 'Active', '2023-09-05'),
(3, 'Data Analyst Intern', 'Analyze business metrics and create reports', 'Python, SQL, Tableau', 'Active', '2023-09-10'),
(4, 'Mobile Developer Intern', 'Develop mobile applications', 'Swift, Kotlin, Flutter', 'Active', '2023-09-15'),
(5, 'DevOps Engineer Intern', 'Maintain CI/CD pipelines', 'Docker, Kubernetes, Jenkins', 'Active', '2023-09-20'),
(1, 'QA Engineer Intern', 'Test software applications', 'Selenium, JUnit, TestNG', 'Active', '2023-09-25'),
(2, 'Machine Learning Intern', 'Build and train ML models', 'Python, TensorFlow, PyTorch', 'Active', '2023-10-01'),
(3, 'Cloud Engineer Intern', 'Manage cloud infrastructure', 'AWS, Azure, GCP', 'Active', '2023-10-05'),
(4, 'Security Engineer Intern', 'Implement security measures', 'Network Security, Cryptography', 'Active', '2023-10-10'),
(5, 'Database Engineer Intern', 'Design and optimize databases', 'MySQL, MongoDB, PostgreSQL', 'Active', '2023-10-15');

-- Database Info (30 records)
INSERT INTO database_info (change_id, staff_id, name, version, type, last_update) VALUES
(1, 1, 'StudentDB', '1.0', 'MySQL', '2023-09-01'),
(2, 2, 'ApplicationDB', '2.0', 'PostgreSQL', '2023-09-05'),
(3, 3, 'ResumeDB', '1.5', 'MongoDB', '2023-09-10'),
(4, 4, 'UserDB', '2.1', 'MySQL', '2023-09-15'),
(5, 5, 'AnalyticsDB', '1.2', 'PostgreSQL', '2023-09-20');

-- Resume Table (45 records - some students have multiple resumes)
INSERT INTO resume (resume_id, user_id, doc_name)
SELECT
    ROW_NUMBER() OVER () as resume_id,
    s.user_id,
    CONCAT('resume_', s.user_id, '_v', FLOOR(1 + RAND() * 3), '.pdf')
FROM student s
CROSS JOIN (SELECT 1 UNION SELECT 2 UNION SELECT 3) n;

-- Suggestion Table (45 records - one for each resume)
INSERT INTO suggestion (suggestion_id, resume_id, suggestion_text)
SELECT
    resume_id,
    resume_id,
    ELT(1 + FLOOR(RAND() * 5),
        'Add more technical skills to your resume',
        'Include GPA in education section',
        'Add more details to project descriptions',
        'Highlight leadership experiences',
        'Update your technical certifications')
FROM resume;

-- Applications (100+ records)
INSERT INTO application (application_id, user_id, position_id, sent_on, status)
SELECT
    ROW_NUMBER() OVER () as application_id,
    s.user_id,
    p.position_id,
    DATE_SUB(CURRENT_DATE, INTERVAL FLOOR(RAND() * 90) DAY),
    ELT(1 + FLOOR(RAND() * 3), 'Pending', 'Accepted', 'Rejected')
FROM student s
CROSS JOIN internship_position p
LIMIT 120;

-- Grade Records (100+ records)
INSERT INTO grade_record (student_id, course_name, grade, recorded_by)
SELECT
    s.user_id,
    c.course_name,
    2 + (RAND() * 2), -- Grades between 2.0 and 4.0
    (SELECT admin_id FROM school_admin ORDER BY RAND() LIMIT 1)
FROM student s
CROSS JOIN (
    SELECT 'Computer Science' as course_name UNION
    SELECT 'Database Systems' UNION
    SELECT 'Web Development' UNION
    SELECT 'Data Structures' UNION
    SELECT 'Algorithms'
) c
LIMIT 120;

-- Co-op Records (100 records)
INSERT INTO co_op_record (student_id, company_name, start_date, end_date, approved_by)
SELECT
    s.user_id,
    c.company_name,
    DATE_SUB(CURRENT_DATE, INTERVAL FLOOR(RAND() * 365) DAY),
    DATE_SUB(CURRENT_DATE, INTERVAL FLOOR(RAND() * 180) DAY),
    (SELECT admin_id FROM school_admin ORDER BY RAND() LIMIT 1)
FROM student s
CROSS JOIN (
    SELECT 'Google' as company_name UNION
    SELECT 'Microsoft' UNION
    SELECT 'Amazon' UNION
    SELECT 'Apple' UNION
    SELECT 'Meta'
) c
LIMIT 100;

-- Data Alteration History
INSERT INTO data_alteration_history (alteration_type, alteration_date, change_id)
SELECT
    ELT(ROW_NUMBER() OVER () % 3 + 1, 'Schema Update', 'Data Migration', 'Index Rebuild'),
    DATE_SUB(CURRENT_DATE, INTERVAL ROW_NUMBER() OVER () DAY),
    change_id
FROM database_info;

-- Backup History
INSERT INTO backup_history (type, backup_date, backup_type, details, change_id)
SELECT
    ELT(ROW_NUMBER() OVER () % 2 + 1, 'Full', 'Incremental'),
    DATE_SUB(CURRENT_DATE, INTERVAL ROW_NUMBER() OVER () DAY),
    ELT(ROW_NUMBER() OVER () % 2 + 1, 'Daily', 'Weekly'),
    'Regular scheduled backup',
    change_id
FROM database_info;

-- Alert History
INSERT INTO alert_history (metrics, alerts, severity, database_id)
SELECT
    'System Performance',
    'Performance threshold exceeded',
    ELT(1 + FLOOR(RAND() * 3), 'Low', 'Medium', 'High'),
    database_id
FROM database_info;

-- Update History
INSERT INTO update_history (update_type, update_date, details, change_id)
SELECT
    'Version Update',
    DATE_SUB(CURRENT_DATE, INTERVAL ROW_NUMBER() OVER () DAY),
    'Regular system update',
    change_id
FROM database_info;

-- Internship Analytics
INSERT INTO internship_analytics (position_id, num_internships, average_apps, database_id)
SELECT
    p.position_id,
    FLOOR(RAND() * 20) + 1,
    FLOOR(RAND() * 50) + 10,
    d.database_id
FROM internship_position p
CROSS JOIN database_info d
LIMIT 30;