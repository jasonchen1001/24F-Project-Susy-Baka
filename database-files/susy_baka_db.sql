DROP DATABASE IF EXISTS project_susy_baka;
CREATE DATABASE project_susy_baka;
USE project_susy_baka;

-- Base tables
CREATE TABLE IF NOT EXISTS user (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    role ENUM('Student', 'School_Admin', 'HR_Manager', 'Maintenance_Staff') NOT NULL,
    dob DATE,
    gender ENUM('Male', 'Female', 'Other')
);

CREATE TABLE IF NOT EXISTS school_admin (
    admin_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    hire_date DATE,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS grade_record (
    grade_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    course_name VARCHAR(100) NOT NULL,
    grade DECIMAL(3, 2) CHECK (grade >= 0.0 AND grade <= 4.0),
    recorded_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    recorded_by INT,
    FOREIGN KEY (recorded_by) REFERENCES school_admin(admin_id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (student_id) REFERENCES user(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS co_op_record (
    co_op_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    company_name VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    approved_by INT,
    FOREIGN KEY (approved_by) REFERENCES school_admin(admin_id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (student_id) REFERENCES user(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS student (
    user_id INT PRIMARY KEY UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS resume (
    resume_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    time_uploaded TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    doc_name VARCHAR(255),
    education TEXT,
    skills TEXT,
    projects TEXT,
    co_op TEXT,
    FOREIGN KEY (user_id) REFERENCES student(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS suggestion (
    suggestion_id INT AUTO_INCREMENT PRIMARY KEY,
    resume_id INT,
    time_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    suggestion_text TEXT,
    FOREIGN KEY (resume_id) REFERENCES resume(resume_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS hr_manager (
    hr_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    user_id INT NOT NULL UNIQUE,
    company_name VARCHAR(100) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

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

CREATE TABLE IF NOT EXISTS application (
    application_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    position_id INT,
    sent_on DATE DEFAULT NULL,
    status ENUM('Pending', 'Accepted', 'Rejected') NOT NULL,
    FOREIGN KEY (user_id) REFERENCES student(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (position_id) REFERENCES internship_position(position_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);
-- Maintenance related tables
CREATE TABLE IF NOT EXISTS maintenance_staff (
    staff_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS database_info (
    database_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    
    staff_id INT NOT NULL,
    name VARCHAR(100),
    version VARCHAR(20),
    type VARCHAR(50),
    last_update DATE,
    
    FOREIGN KEY (staff_id) REFERENCES maintenance_staff(staff_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS data_alteration_history (
    alteration_type VARCHAR(100),
    alteration_date DATE,
    database_id INT NOT NULL,
    FOREIGN KEY (database_id) REFERENCES database_info(database_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS backup_history (
    type VARCHAR(50),
    backup_date DATE,
    backup_type VARCHAR(100),
    details VARCHAR(255),
    database_id INT NOT NULL,
    FOREIGN KEY (database_id) REFERENCES database_info(database_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS alert_history (
    metrics VARCHAR(255),
    alerts VARCHAR(255),
    severity VARCHAR(255),
    database_id INT NOT NULL,
    FOREIGN KEY (database_id) REFERENCES database_info(database_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS update_history (
    update_type VARCHAR(100),
    update_date DATE,
    details VARCHAR(255),
    database_id INT NOT NULL,
    FOREIGN KEY (database_id) REFERENCES database_info(database_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS internship_analytics (
    position_id INT,
    num_internships INT,
    average_apps INT,
    database_id INT NOT NULL,
    FOREIGN KEY (database_id) REFERENCES database_info(database_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (position_id) REFERENCES internship_position(position_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);
-- Triggers for resume synchronization
DELIMITER //

CREATE TRIGGER update_resume_after_grade_change
AFTER INSERT ON grade_record
FOR EACH ROW
BEGIN
    IF NEW.course_name = 'Computer Science Major GPA' THEN
        UPDATE resume r
        SET education = CONCAT(
            'Bachelor of Science in Computer Science, GPA: ',
            FORMAT(NEW.grade, 2)
        )
        WHERE r.user_id = NEW.student_id;
    END IF;
END//

CREATE TRIGGER update_resume_grade_on_update
AFTER UPDATE ON grade_record
FOR EACH ROW
BEGIN
    IF NEW.course_name = 'Computer Science Major GPA' THEN
        UPDATE resume r
        SET education = CONCAT(
            'Bachelor of Science in Computer Science, GPA: ',
            FORMAT(NEW.grade, 2)
        )
        WHERE r.user_id = NEW.student_id;
    END IF;
END//

CREATE TRIGGER update_resume_after_coop_change
AFTER INSERT ON co_op_record
FOR EACH ROW
BEGIN
    UPDATE resume r
    SET co_op = (
        SELECT GROUP_CONCAT(
            CONCAT(
                company_name,
                ' (',
                DATE_FORMAT(start_date, '%b %Y'),
                ' - ',
                DATE_FORMAT(end_date, '%b %Y'),
                ')'
            )
            ORDER BY start_date DESC
            SEPARATOR '; '
        )
        FROM co_op_record
        WHERE student_id = NEW.student_id
        GROUP BY student_id
    )
    WHERE r.user_id = NEW.student_id;
END//

CREATE TRIGGER update_resume_after_coop_update
AFTER UPDATE ON co_op_record
FOR EACH ROW
BEGIN
    UPDATE resume r
    SET co_op = (
        SELECT GROUP_CONCAT(
            CONCAT(
                company_name,
                ' (',
                DATE_FORMAT(start_date, '%b %Y'),
                ' - ',
                DATE_FORMAT(end_date, '%b %Y'),
                ')'
            )
            ORDER BY start_date DESC
            SEPARATOR '; '
        )
        FROM co_op_record
        WHERE student_id = NEW.student_id
        GROUP BY student_id
    )
    WHERE r.user_id = NEW.student_id;
END//

CREATE TRIGGER update_resume_after_coop_delete
AFTER DELETE ON co_op_record
FOR EACH ROW
BEGIN
    UPDATE resume r
    SET co_op = COALESCE(
        (SELECT GROUP_CONCAT(
            CONCAT(
                company_name,
                ' (',
                DATE_FORMAT(start_date, '%b %Y'),
                ' - ',
                DATE_FORMAT(end_date, '%b %Y'),
                ')'
            )
            ORDER BY start_date DESC
            SEPARATOR '; '
        )
        FROM co_op_record
        WHERE student_id = OLD.student_id
        GROUP BY student_id),
        'No internship experience'
    )
    WHERE r.user_id = OLD.student_id;
END//

DELIMITER ;

-- Insert base user data
INSERT INTO user (full_name, email, role, dob, gender) VALUES
-- Students
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

-- School Admins
('William Smith', 'william.s@school.com', 'School_Admin', '1980-03-12', 'Male'),
('Emma Davis', 'emma.d@school.com', 'School_Admin', '1975-11-22', 'Female'),
('James Wilson', 'james.w@school.com', 'School_Admin', '1978-07-15', 'Male'),
('Sarah Johnson', 'sarah.j@school.com', 'School_Admin', '1982-09-30', 'Female'),
('Robert Brown', 'robert.b@school.com', 'School_Admin', '1977-05-20', 'Male'),
('Mary Williams', 'mary.w@school.com', 'School_Admin', '1981-12-05', 'Female'),
('David Miller', 'david.m@school.com', 'School_Admin', '1979-08-18', 'Male'),
('Patricia Davis', 'patricia.d@school.com', 'School_Admin', '1983-02-28', 'Female'),

-- HR Managers
('John Anderson', 'john.a@hr.com', 'HR_Manager', '1985-06-18', 'Male'),
('Lisa Taylor', 'lisa.t@hr.com', 'HR_Manager', '1982-02-25', 'Female'),
('Mark Thompson', 'mark.t@hr.com', 'HR_Manager', '1984-10-12', 'Male'),
('Karen White', 'karen.w@hr.com', 'HR_Manager', '1983-04-15', 'Female'),
('Paul Martin', 'paul.m@hr.com', 'HR_Manager', '1981-09-08', 'Male'),

-- Maintenance Staff
('Thomas Anderson', 'thomas.a@maintenance.com', 'Maintenance_Staff', '1978-08-01', 'Male'),
('Susan Clark', 'susan.c@maintenance.com', 'Maintenance_Staff', '1980-04-14', 'Female'),
('Richard Lee', 'richard.l@maintenance.com', 'Maintenance_Staff', '1979-11-27', 'Male'),
('Jennifer Hall', 'jennifer.h@maintenance.com', 'Maintenance_Staff', '1981-06-23', 'Female'),
('Daniel King', 'daniel.k@maintenance.com', 'Maintenance_Staff', '1977-12-09', 'Male');

-- Insert data into role-specific tables
INSERT INTO student (user_id, full_name, email)
SELECT user_id, full_name, email
FROM user
WHERE role = 'Student';

INSERT INTO school_admin (user_id, full_name, hire_date)
SELECT user_id, full_name, DATE_SUB(CURRENT_DATE, INTERVAL FLOOR(RAND() * 1825) DAY)
FROM user
WHERE role = 'School_Admin';

INSERT INTO hr_manager (user_id, full_name, email, company_name)
SELECT
    user_id,
    full_name,
    email,
    CASE user_id
        WHEN 29 THEN 'Google'
        WHEN 30 THEN 'Amazon'
        WHEN 31 THEN 'Microsoft'
        WHEN 32 THEN 'Apple'
        WHEN 33 THEN 'Meta'
        ELSE 'Default Company'
    END AS company_name
FROM user
WHERE role = 'HR_Manager';

INSERT INTO maintenance_staff (user_id, full_name)
SELECT user_id, full_name
FROM user
WHERE role = 'Maintenance_Staff';

-- Insert grade records
INSERT INTO grade_record (student_id, course_name, grade, recorded_by)
SELECT
    s.user_id,
    'Computer Science Major GPA',
    2.8 + (RAND() * 1.2),
    (SELECT admin_id FROM school_admin ORDER BY RAND() LIMIT 1)
FROM student s
LIMIT 20;

-- Insert co-op records with non-overlapping dates

INSERT INTO co_op_record (student_id, company_name, start_date, end_date, approved_by) VALUES

(1, 'Google', '2023-06-01', '2023-08-31', 1),
(1, 'Microsoft', '2022-06-01', '2022-08-31', 2),
(2, 'Amazon', '2023-06-01', '2023-08-31', 1),
(3, 'Apple', '2023-06-01', '2023-08-31', 3),
(3, 'TechStart Solutions', '2022-06-01', '2022-08-31', 2),
(4, 'Meta', '2023-06-01', '2023-08-31', 4),
(5, 'ByteCraft Solutions', '2023-06-01', '2023-08-31', 1),
(5, 'Adobe', '2022-06-01', '2022-08-31', 3),


(6, 'LinkedIn', '2023-06-01', '2023-08-31', 2),
(6, 'Google', '2022-06-01', '2022-08-31', 1),
(7, 'Salesforce', '2023-06-01', '2023-08-31', 4),
(8, 'DataFlow Systems', '2023-06-01', '2023-08-31', 1),
(8, 'Microsoft', '2022-06-01', '2022-08-31', 2),
(9, 'Innovation Labs', '2023-06-01', '2023-08-31', 3),
(10, 'Twitter', '2023-06-01', '2023-08-31', 2),


(11, 'Amazon', '2023-06-01', '2023-08-31', 1),
(11, 'SmartCode Inc', '2022-06-01', '2022-08-31', 4),
(12, 'Apple', '2023-06-01', '2023-08-31', 2),
(13, 'Meta', '2023-06-01', '2023-08-31', 3),
(13, 'CloudMind Tech', '2022-06-01', '2022-08-31', 1),
(14, 'Digital Frontiers', '2023-06-01', '2023-08-31', 4),
(15, 'Adobe', '2023-06-01', '2023-08-31', 2),


(16, 'Uber', '2023-06-01', '2023-08-31', 1),
(16, 'WebFlow Systems', '2022-06-01', '2022-08-31', 3),
(17, 'Salesforce', '2023-06-01', '2023-08-31', 2),
(18, 'Agile Dynamics', '2023-06-01', '2023-08-31', 4),
(18, 'LinkedIn', '2022-06-01', '2022-08-31', 1),
(19, 'NextGen Software', '2023-06-01', '2023-08-31', 3),
(20, 'Twitter', '2023-06-01', '2023-08-31', 2),
(20, 'Innovation Labs', '2022-06-01', '2022-08-31', 4);

-- Insert basic resume data
INSERT INTO resume (user_id, doc_name, skills, projects)
SELECT
    s.user_id,
    CONCAT('resume_', REPLACE(LOWER(s.full_name), ' ', '_'), '.pdf'),
    CONCAT(
        ELT(FLOOR(RAND() * 6) + 1, 'Python', 'Java', 'C++', 'JavaScript', 'Ruby', 'PHP'),
        ', ',
        ELT(FLOOR(RAND() * 6) + 1, 'React', 'Angular', 'Vue.js', 'Node.js', 'Django', 'Flask'),
        ', ',
        ELT(FLOOR(RAND() * 6) + 1, 'SQL', 'MongoDB', 'PostgreSQL', 'MySQL', 'OracleDB', 'Redis')
    ) as skills,
    CONCAT(
        ELT(FLOOR(RAND() * 6) + 1,
            'Developed a Personal Finance Tracker App',
            'Built a Machine Learning Model for Sentiment Analysis',
            'Designed a Collaborative Team Task Management System',
            'Implemented an E-commerce Platform with Payment Integration',
            'Created a Social Media Platform for Hobby Communities',
            'Optimized a Blog Website for SEO and Scalability')
    ) as projects
FROM student s
WHERE s.user_id <= 20;

-- Update resume education and co-op fields based on existing records
UPDATE resume r
INNER JOIN grade_record g ON r.user_id = g.student_id
SET r.education = CONCAT(
    'Bachelor of Science in Computer Science, GPA: ',
    FORMAT(g.grade, 2)
)
WHERE g.course_name = 'Computer Science Major GPA';

UPDATE resume r
SET r.co_op = (
    SELECT GROUP_CONCAT(
        CONCAT(
            c.company_name,
            ' (',
            DATE_FORMAT(c.start_date, '%b %Y'),
            ' - ',
            DATE_FORMAT(c.end_date, '%b %Y'),
            ')'
        )
        ORDER BY c.start_date DESC
        SEPARATOR '; '
    )
    FROM co_op_record c
    WHERE c.student_id = r.user_id
    GROUP BY c.student_id
)
WHERE r.user_id IN (SELECT DISTINCT student_id FROM co_op_record);

-- Insert internship positions
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

-- Insert resume suggestions
INSERT INTO suggestion (resume_id, suggestion_text) VALUES
(1, 'Your GPA of 3.40 is competitive. Consider elaborating on specific modules or algorithms you implemented in the Task Management System. With experience at major tech companies, highlight any cross-team collaboration and quantifiable impacts from your projects.'),
(2, 'Strong GPA of 3.62 shows academic excellence. For the blog optimization project, include specific metrics like improved load times or SEO rankings. With your MongoDB skills, mention any database optimization techniques you implemented.'),
(3, 'Exceptional GPA of 3.85 is impressive. With your diverse internship experience across Salesforce, Google, and Intel, highlight how you applied your PHP and SQL skills in different enterprise environments. Include specific contributions to each company.'),
(4, 'Consider highlighting how you used MongoDB in your social media platform project. With experience at Airbnb, Apple, and Amazon, emphasize any scalability challenges you solved. Your 3.55 GPA demonstrates strong academic performance.'),
(5, 'Your Angular and Java combination is valuable for enterprise development. With experience at LinkedIn and Microsoft, detail any feature implementations that impacted user engagement. Your 3.62 GPA strengthens your profile.'),
(6, 'For your e-commerce platform, detail specific payment systems you integrated. Your Python and Django skills align well with your backend experience. Quantify the transaction volumes or performance improvements you achieved.'),
(7, 'Strong technical foundation with C++ and Meta experience. Consider adding metrics about the Finance Tracker App\'s user base or performance. Detail how you used OracleDB for data management.'),
(8, 'Focus on explaining the machine learning models you built, including accuracy rates and real-world applications. Your internships at Salesforce and IBM provide good enterprise experience - highlight specific projects and their impact.'),
(9, 'In your e-commerce platform experience, quantify the scale of transactions processed. With Meta and Salesforce experience, highlight any cloud infrastructure or scalability improvements you implemented.'),
(10, 'Your PHP and MySQL skills could be highlighted with specific performance optimizations. Detail the payment integration methods in your e-commerce project. Consider adding metrics from your Intel and Apple internships.'),
(11, 'Highlight specific SEO improvements achieved in your blog optimization project. Your experience with Microsoft could be enhanced by mentioning specific technologies used. Consider adding metrics to demonstrate impact.'),
(12, 'Strong mix of front-end and database skills. With experience at Microsoft and Oracle, highlight any enterprise-scale challenges you solved. Add specific examples of Node.js implementations.'),
(13, 'Excellent 3.78 GPA shows strong academic foundation. For your social media platform, detail user engagement metrics or scalability solutions. Highlight specific contributions at Amazon and Apple.'),
(14, 'Outstanding 3.81 GPA is a strong differentiator. Consider adding specific features you implemented in the Task Management System. Detail how you used Django and MySQL together for scalability.'),
(15, 'Strong JavaScript and Redis expertise. For your e-commerce platform, include performance metrics and scalability solutions. Your Amazon experience could be enhanced with specific project outcomes.'),
(16, 'Your experience with React and MongoDB is valuable. Add metrics about the Task Management System\'s user base or performance improvements. Detail specific contributions at Oracle and Microsoft.'),
(17, 'Exceptional 3.95 GPA is remarkable. For your machine learning project, include accuracy rates and real-world applications. Highlight specific technologies used during your Intel and IBM internships.'),
(18, 'Your Java and Angular skills align well with enterprise development. Detail specific features implemented in the Task Management System. Consider adding metrics from your Meta internship experience.'),
(19, 'Strong Python and Django combination. Consider adding user metrics or performance improvements from your Task Management System. Detail specific projects at Airbnb and Salesforce.'),
(20, 'Good balance of front-end and back-end skills. For your e-commerce platform, include transaction volumes or performance metrics. Highlight specific contributions at Adobe and LinkedIn.');

-- Insert applications
INSERT INTO application (user_id, position_id, sent_on, status)
SELECT
    s.user_id,
    p.position_id,
    DATE_SUB(CURRENT_DATE, INTERVAL FLOOR(RAND() * 90) DAY),
    ELT(1 + FLOOR(RAND() * 3), 'Pending', 'Accepted', 'Rejected')
FROM student s
CROSS JOIN internship_position p
LIMIT 120;

-- Insert maintenance related data
INSERT INTO database_info (database_id, staff_id, name, version, type, last_update) VALUES
(1, 1, 'StudentDB', '1.0', 'MySQL', '2023-09-01'),
(2, 2, 'ApplicationDB', '2.0', 'PostgreSQL', '2023-09-05'),
(3, 3, 'ResumeDB', '1.5', 'MongoDB', '2023-09-10'),
(4, 4, 'UserDB', '2.1', 'MySQL', '2023-09-15'),
(5, 5, 'AnalyticsDB', '1.2', 'PostgreSQL', '2023-09-20');

-- Insert history records
INSERT INTO data_alteration_history (alteration_type, alteration_date, database_id)
SELECT
    ELT(ROW_NUMBER() OVER () % 3 + 1, 'Schema Update', 'Data Migration', 'Index Rebuild'),
    DATE_SUB(CURRENT_DATE, INTERVAL ROW_NUMBER() OVER () DAY),
    database_id
FROM database_info;

INSERT INTO backup_history (type, backup_date, backup_type, details, database_id)
SELECT
    ELT(ROW_NUMBER() OVER () % 2 + 1, 'Full', 'Incremental'),
    DATE_SUB(CURRENT_DATE, INTERVAL ROW_NUMBER() OVER () DAY),
    ELT(ROW_NUMBER() OVER () % 2 + 1, 'Daily', 'Weekly'),
    'Regular scheduled backup',
    database_id
FROM database_info;

INSERT INTO alert_history (metrics, alerts, severity, database_id)
SELECT
    'System Performance',
    'Performance threshold exceeded',
    ELT(1 + FLOOR(RAND() * 3), 'Low', 'Medium', 'High'),
    database_id
FROM database_info;

INSERT INTO update_history (update_type, update_date, details, database_id)
SELECT
    'Version Update',
    DATE_SUB(CURRENT_DATE, INTERVAL ROW_NUMBER() OVER () DAY),
    'Regular system update',
    database_id
FROM database_info;

INSERT INTO internship_analytics (position_id, num_internships, average_apps, database_id)
SELECT
    p.position_id,
    FLOOR(RAND() * 20) + 1,
    FLOOR(RAND() * 50) + 10,
    d.database_id
FROM internship_position p
CROSS JOIN database_info d
LIMIT 30;

UPDATE grade_record
SET grade = 3.4
WHERE student_id = 1 AND course_name = 'Computer Science Major GPA';

UPDATE co_op_record
SET company_name = 'Google',
    start_date = '2023-03-01',
    end_date = '2023-05-31'
WHERE student_id = 1 AND company_name = 'Meta';
<<<<<<< HEAD

=======
>>>>>>> b69dd6d2bc3bbc429a8d36ef468dffba3992421f
