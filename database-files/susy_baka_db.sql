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
    first_name VARCHAR(50),
    mid_name VARCHAR(50),
    last_name VARCHAR(50),
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

-- Insert data into the user table (2 for each role)
INSERT INTO user (full_name, email, role, dob, gender)
VALUES
('Alice Johnson', 'alice.johnson@student.com', 'Student', '2001-05-15', 'Female'), -- Student 1
('Bob Smith', 'bob.smith@student.com', 'Student', '2000-09-20', 'Male'),          -- Student 2
('John Doe', 'john.doe@school.com', 'School_Admin', '1980-03-12', 'Male'),        -- School Admin 1
('Jane Brown', 'jane.brown@school.com', 'School_Admin', '1975-11-22', 'Female'),  -- School Admin 2
('Emily Davis', 'emily.davis@hr.com', 'HR_Manager', '1985-06-18', 'Female'),      -- HR Manager 1
('Michael Scott', 'michael.scott@hr.com', 'HR_Manager', '1982-02-25', 'Male'),    -- HR Manager 2
('Sarah Connor', 'sarah.connor@maintenance.com', 'Maintenance_Staff', '1978-08-01', 'Female'), -- Maintenance Staff 1
('James Cameron', 'james.cameron@maintenance.com', 'Maintenance_Staff', '1980-04-14', 'Male'); -- Maintenance Staff 2

-- Insert data into the school_admin table (2 administrators)
INSERT INTO school_admin (admin_id, user_id, hire_date)
VALUES
(3, 3, '2015-08-01'), -- Admin John Doe
(4, 4, '2020-01-15'); -- Admin Jane Brown

-- Insert data into the grade_record table (grades for 2 students recorded by different admins)
INSERT INTO grade_record (student_id, course_name, grade, recorded_by)
VALUES
(1, 'Mathematics', 3.8, 3), -- Alice's grade recorded by John Doe
(2, 'Physics', 3.6, 4),     -- Bob's grade recorded by Jane Brown
(1, 'Chemistry', 3.9, 3);   -- Alice's grade recorded by John Doe

-- Insert data into the co_op_record table (internship records for students approved by different admins)
INSERT INTO co_op_record (student_id, company_name, start_date, end_date, approved_by)
VALUES
(1, 'TechCorp', '2023-06-01', '2023-08-31', 3), -- Alice's internship approved by John Doe
(2, 'Innovate Inc', '2023-07-01', '2023-09-30', 4); -- Bob's internship approved by Jane Brown

-- Insert data into the student table (2 students)
INSERT INTO student (user_id, full_name, email)
VALUES
(1, 'Alice Johnson', 'alice.johnson@student.com'), -- Student 1
(2, 'Bob Smith', 'bob.smith@student.com');         -- Student 2

-- Insert data into the application table (applications for internships by students)
INSERT INTO application (application_id, user_id, position_id, sent_on, status)
VALUES
(1, 1, 101, '2023-10-01', 'Pending'), -- Alice's application for Position 101
(2, 2, 102, '2023-10-05', 'Accepted'); -- Bob's application for Position 102

-- Insert data into the resume table (2 resumes for students)
INSERT INTO resume (resume_id, user_id, time_uploaded, doc_name)
VALUES
(1, 1, NOW(), 'alice_resume.pdf'), -- Alice's resume
(2, 2, NOW(), 'bob_resume.pdf');   -- Bob's resume

-- Insert data into the suggestion table (suggestions for student resumes)
INSERT INTO suggestion (suggestion_id, resume_id, time_created, suggestion_text)
VALUES
(1, 1, NOW(), 'Add more technical skills'), -- Suggestion for Alice's resume
(2, 2, NOW(), 'Highlight leadership experience'); -- Suggestion for Bob's resume

-- Insert data into the hr_manager table (2 HR managers)
INSERT INTO hr_manager (user_id, full_name, email)
VALUES
(5, 'Emily Davis', 'emily.davis@hr.com'),   -- HR Manager 1
(6, 'Michael Scott', 'michael.scott@hr.com'); -- HR Manager 2

-- Insert data into the internship_position table (positions created by HR managers)
INSERT INTO internship_position (hr_id, title, description, requirements, status, posted_date)
VALUES
(1, 'Backend Developer Intern', 'Develop APIs and manage databases.', 'Java, MySQL', 'Active', '2023-09-01'), -- Position by Emily
(2, 'Frontend Developer Intern', 'Build user interfaces.', 'HTML, CSS, JavaScript', 'Active', '2023-09-15'); -- Position by Michael

-- Insert data into the maintenance_staff table (2 maintenance staff members)
INSERT INTO maintenance_staff (user_id, first_name, mid_name, last_name)
VALUES
(7, 'Sarah', 'L.', 'Connor'), -- Maintenance Staff Sarah
(8, 'James', 'T.', 'Cameron'); -- Maintenance Staff James

-- Insert data into the database_info table (databases managed by maintenance staff)
INSERT INTO database_info (change_id, staff_id, name, version, type, last_update)
VALUES
(1, 1, 'MainDB', '1.0', 'Relational', '2023-10-01'),
(2, 2, 'BackupDB', '1.0', 'Backup', '2023-10-10');

-- Insert data into the data_alteration_history table (alteration records)
INSERT INTO data_alteration_history (alteration_type, alteration_date, change_id)
VALUES
('Index Rebuild', '2023-10-15', 1),
('Data Cleanup', '2023-10-20', 2);

-- Insert data into the backup_history table (backup records)
INSERT INTO backup_history (type, backup_date, backup_type, details, change_id)
VALUES
('Full', '2023-10-10', 'Weekly', 'Weekly full backup completed.', 2),
('Incremental', '2023-10-17', 'Daily', 'Incremental backup completed.', 2);

-- Insert data into the alert_history table (alerts for databases)
INSERT INTO alert_history (metrics, alerts, severity, database_id)
VALUES
('CPU Usage', 'High CPU usage detected', 'High', 1),
('Disk Space', 'Low disk space warning', 'Medium', 2);

-- Insert data into the update_history table (update records)
INSERT INTO update_history (update_type, update_date, details, change_id)
VALUES
('Version Upgrade', '2023-10-12', 'Upgraded MainDB to version 1.1.', 1),
('Security Patch', '2023-10-18', 'Applied security patch.', 2);

-- Insert data into the internship_analytics table (analytics for positions)
INSERT INTO internship_analytics (position_id, num_internships, average_apps, database_id)
VALUES
(1, 5, 3, 1),
(2, 8, 5, 1);

/* 1. Student
User Stories:
- Upload and edit resumes.
- View application history.
- Update application status.
- Delete unnecessary resumes.
*/

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

/* 2. School Admin
User Stories:
- Manage student records.
- Update student academic grades.
- Delete invalid student records.
- Query student academic performance.
*/

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

/* 3. HR Manager
User Stories:
- Post and edit internship positions.
- Delete inactive job postings.
- Query the number of applicants for each position.
- Automatically filter resumes.
*/

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

/* 4. Maintenance Staff
User Stories:
- Add data cleansing tasks.
- Remove expired backups.
- Monitor system performance.
- Add new databases.
*/

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
-- Additional sample data INSERT statements
-- Add after your existing INSERT statements

-- Additional users (mix of roles)
INSERT INTO user (full_name, email, role, dob, gender) VALUES
-- More Students
('Peter Parker', 'peter.p@student.com', 'Student', '2002-08-10', 'Male'),
('Mary Jane', 'mary.j@student.com', 'Student', '2002-06-15', 'Female'),
('Harry Osborn', 'harry.o@student.com', 'Student', '2002-07-20', 'Male'),
('Gwen Stacy', 'gwen.s@student.com', 'Student', '2002-05-25', 'Female'),
('Flash Thompson', 'flash.t@student.com', 'Student', '2002-04-30', 'Male'),
('Betty Brant', 'betty.b@student.com', 'Student', '2002-03-05', 'Female'),
('Ned Leeds', 'ned.l@student.com', 'Student', '2002-02-10', 'Male'),
('Liz Allan', 'liz.a@student.com', 'Student', '2002-01-15', 'Female'),
('Miles Morales', 'miles.m@student.com', 'Student', '2002-12-20', 'Male'),
('Cindy Moon', 'cindy.m@student.com', 'Student', '2002-11-25', 'Female'),
('Eugene Thompson', 'eugene.t@student.com', 'Student', '2002-10-30', 'Male'),
('Sally Avril', 'sally.a@student.com', 'Student', '2002-09-05', 'Female'),
('Kenny Kong', 'kenny.k@student.com', 'Student', '2002-08-10', 'Male'),
('Glory Grant', 'glory.g@student.com', 'Student', '2002-07-15', 'Female'),
('Randy Robertson', 'randy.r@student.com', 'Student', '2002-06-20', 'Male'),
('Debra Whitman', 'debra.w@student.com', 'Student', '2002-05-25', 'Female'),
('Jason Ionello', 'jason.i@student.com', 'Student', '2002-04-30', 'Male'),
('Tiny McKeever', 'tiny.m@student.com', 'Student', '2002-03-05', 'Male'),
('Charlie Murphy', 'charlie.m@student.com', 'Student', '2002-02-10', 'Male'),
('Jessica Jones', 'jessica.j@student.com', 'Student', '2002-01-15', 'Female'),

-- More School Admins
('Charles Xavier', 'charles.x@school.com', 'School_Admin', '1975-09-15', 'Male'),
('Jean Grey', 'jean.g@school.com', 'School_Admin', '1980-03-20', 'Female'),
('Scott Summers', 'scott.s@school.com', 'School_Admin', '1978-07-25', 'Male'),
('Emma Frost', 'emma.f@school.com', 'School_Admin', '1982-11-30', 'Female'),
('Henry McCoy', 'henry.m@school.com', 'School_Admin', '1976-05-05', 'Male'),
('Ororo Munroe', 'ororo.m@school.com', 'School_Admin', '1979-01-10', 'Female'),
('Logan Howlett', 'logan.h@school.com', 'School_Admin', '1977-04-15', 'Male'),
('Kitty Pryde', 'kitty.p@school.com', 'School_Admin', '1981-08-20', 'Female'),

-- More HR Managers
('Tony Stark', 'tony.s@hr.com', 'HR_Manager', '1970-05-29', 'Male'),
('Pepper Potts', 'pepper.p@hr.com', 'HR_Manager', '1975-08-15', 'Female'),
('Happy Hogan', 'happy.h@hr.com', 'HR_Manager', '1972-11-20', 'Male'),
('Maria Hill', 'maria.h@hr.com', 'HR_Manager', '1977-02-25', 'Female'),
('Phil Coulson', 'phil.c@hr.com', 'HR_Manager', '1974-06-30', 'Male'),
('Nick Fury', 'nick.f@hr.com', 'HR_Manager', '1969-09-05', 'Male'),
('Sharon Carter', 'sharon.c@hr.com', 'HR_Manager', '1976-12-10', 'Female'),
('James Rhodes', 'james.r@hr.com', 'HR_Manager', '1973-03-15', 'Male'),

-- More Maintenance Staff
('Bruce Banner', 'bruce.b@maintenance.com', 'Maintenance_Staff', '1980-12-18', 'Male'),
('Betty Ross', 'betty.r@maintenance.com', 'Maintenance_Staff', '1982-03-23', 'Female'),
('Leonard Samson', 'leonard.s@maintenance.com', 'Maintenance_Staff', '1981-06-28', 'Male'),
('Rick Jones', 'rick.j@maintenance.com', 'Maintenance_Staff', '1983-09-02', 'Male'),
('Jennifer Walters', 'jennifer.w@maintenance.com', 'Maintenance_Staff', '1984-12-07', 'Female'),
('Samuel Sterns', 'samuel.s@maintenance.com', 'Maintenance_Staff', '1979-03-12', 'Male'),
('Glenn Talbot', 'glenn.t@maintenance.com', 'Maintenance_Staff', '1978-06-17', 'Male');

-- Additional school_admin records
INSERT INTO school_admin (user_id, hire_date)
SELECT user_id, DATE_SUB(CURRENT_DATE, INTERVAL FLOOR(RAND() * 3650) DAY)
FROM user
WHERE role = 'School_Admin'
AND user_id NOT IN (SELECT user_id FROM school_admin);

-- Additional student records
INSERT INTO student (user_id, full_name, email)
SELECT user_id, full_name, email
FROM user
WHERE role = 'Student'
AND user_id NOT IN (SELECT user_id FROM student);

-- Additional hr_manager records
INSERT INTO hr_manager (user_id, full_name, email)
SELECT user_id, full_name, email
FROM user
WHERE role = 'HR_Manager'
AND user_id NOT IN (SELECT user_id FROM hr_manager);

-- Additional maintenance_staff records
INSERT INTO maintenance_staff (user_id, first_name, mid_name, last_name)
SELECT
    user_id,
    SUBSTRING_INDEX(full_name, ' ', 1),
    NULL,
    SUBSTRING_INDEX(full_name, ' ', -1)
FROM user
WHERE role = 'Maintenance_Staff'
AND user_id NOT IN (SELECT user_id FROM maintenance_staff);

-- Additional grade records
INSERT INTO grade_record (student_id, course_name, grade, recorded_by)
SELECT
    s.user_id,
    course,
    ROUND(2 + (RAND() * 2), 2),
    (SELECT admin_id FROM school_admin ORDER BY RAND() LIMIT 1)
FROM student s
CROSS JOIN (
    SELECT 'Computer Science' as course UNION ALL
    SELECT 'Database Systems' UNION ALL
    SELECT 'Web Development' UNION ALL
    SELECT 'Data Structures' UNION ALL
    SELECT 'Algorithms' UNION ALL
    SELECT 'Software Engineering' UNION ALL
    SELECT 'Machine Learning' UNION ALL
    SELECT 'Artificial Intelligence' UNION ALL
    SELECT 'Operating Systems' UNION ALL
    SELECT 'Computer Networks'
) courses
LIMIT 45;

-- Additional co_op records
INSERT INTO co_op_record (student_id, company_name, start_date, end_date, approved_by)
SELECT
    s.user_id,
    company,
    start_date,
    DATE_ADD(start_date, INTERVAL 3 MONTH),
    (SELECT admin_id FROM school_admin ORDER BY RAND() LIMIT 1)
FROM student s
CROSS JOIN (
    SELECT 'Google' as company, '2023-05-01' as start_date UNION ALL
    SELECT 'Microsoft', '2023-05-15' UNION ALL
    SELECT 'Amazon', '2023-06-01' UNION ALL
    SELECT 'Apple', '2023-06-15' UNION ALL
    SELECT 'Meta', '2023-07-01' UNION ALL
    SELECT 'Netflix', '2023-07-15' UNION ALL
    SELECT 'Twitter', '2023-08-01' UNION ALL
    SELECT 'LinkedIn', '2023-08-15' UNION ALL
    SELECT 'Uber', '2023-09-01' UNION ALL
    SELECT 'Airbnb', '2023-09-15'
) companies
LIMIT 45;

-- Additional internship positions
INSERT INTO internship_position (hr_id, title, description, requirements, status, posted_date)
VALUES
(1, 'AI/ML Engineer Intern', 'Work on machine learning models and AI applications', 'Python, TensorFlow, PyTorch', 'Active', '2023-08-01'),
(2, 'Cloud Developer Intern', 'Develop cloud-native applications', 'AWS, Docker, Kubernetes', 'Active', '2023-08-15'),
(3, 'Data Engineer Intern', 'Build data pipelines and ETL processes', 'SQL, Python, Apache Spark', 'Active', '2023-09-01'),
(1, 'DevOps Engineer Intern', 'Manage CI/CD pipelines and infrastructure', 'Jenkins, Docker, Kubernetes', 'Active', '2023-09-15'),
(2, 'Mobile App Developer Intern', 'Develop mobile applications', 'Swift, Kotlin, React Native', 'Active', '2023-10-01'),
(3, 'Security Engineer Intern', 'Work on cybersecurity projects', 'Network Security, Cryptography', 'Active', '2023-10-15'),
(1, 'UI/UX Designer Intern', 'Design user interfaces and experiences', 'Figma, Adobe XD, Sketch', 'Active', '2023-11-01'),
(2, 'Quality Assurance Intern', 'Test software applications', 'Selenium, JUnit, TestNG', 'Active', '2023-11-15');

-- Additional applications (100+ records)
INSERT INTO application (application_id, user_id, position_id, sent_on, status)
SELECT
    ROW_NUMBER() OVER () + 100 as application_id,
    s.user_id,
    p.position_id,
    DATE_SUB(CURRENT_DATE, INTERVAL FLOOR(RAND() * 90) DAY),
    ELT(1 + FLOOR(RAND() * 3), 'Pending', 'Accepted', 'Rejected')
FROM student s
CROSS JOIN internship_position p
WHERE p.status = 'Active'
LIMIT 100;

-- Additional resumes
INSERT INTO resume (resume_id, user_id, time_uploaded, doc_name)
SELECT
    ROW_NUMBER() OVER () + 100 as resume_id,
    user_id,
    DATE_SUB(CURRENT_DATE, INTERVAL FLOOR(RAND() * 180) DAY),
    CONCAT('resume_', user_id, '_v', FLOOR(RAND() * 5), '.pdf')
FROM student
CROSS JOIN (SELECT 1 UNION SELECT 2) n
LIMIT 45;

-- Additional suggestions
INSERT INTO suggestion (suggestion_id, resume_id, time_created, suggestion_text)
SELECT
    ROW_NUMBER() OVER () + 100 as suggestion_id,
    resume_id,
    CURRENT_TIMESTAMP,
    CASE FLOOR(RAND() * 5)
        WHEN 0 THEN 'Add more programming languages to skills section'
        WHEN 1 THEN 'Include GPA in education section'
        WHEN 2 THEN 'Add more details to project descriptions'
        WHEN 3 THEN 'Highlight leadership roles in activities'
        ELSE 'Update technical skills with latest technologies'
    END
FROM resume
LIMIT 45;