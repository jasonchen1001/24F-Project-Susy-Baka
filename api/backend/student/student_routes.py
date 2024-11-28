from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

student = Blueprint('student', __name__)

#------------------------------------------------------------
# Get student personal information
@student.route('/info/<int:user_id>', methods=['GET'])
def get_student_info(user_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT s.user_id, s.full_name, s.email, u.dob, u.gender,
                   r.education, r.skills, r.projects, r.co_op
            FROM student s
            JOIN user u ON s.user_id = u.user_id
            LEFT JOIN resume r ON s.user_id = r.user_id
            WHERE s.user_id = %s
            ORDER BY r.time_uploaded DESC
            LIMIT 1
        ''', (user_id,))
        student_info = cursor.fetchone()
        
        if not student_info:
            return make_response(jsonify({'error': 'Student not found'}), 404)
            
        return make_response(jsonify(student_info), 200)
    except Exception as e:
        current_app.logger.error(f'Error in get_student_info: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Get student grades
@student.route('/grades/<int:user_id>', methods=['GET'])
def get_student_grades(user_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT grade_id, course_name, grade, recorded_date
            FROM grade_record
            WHERE student_id = %s
            ORDER BY recorded_date DESC
        ''', (user_id,))
        grades = cursor.fetchall()
        return make_response(jsonify(grades), 200)
    except Exception as e:
        current_app.logger.error(f'Error in get_student_grades: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Get student co-op records
@student.route('/coops/<int:user_id>', methods=['GET'])
def get_student_coops(user_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT co_op_id, company_name, start_date, end_date
            FROM co_op_record
            WHERE student_id = %s
            ORDER BY start_date DESC
        ''', (user_id,))
        coops = cursor.fetchall()
        return make_response(jsonify(coops), 200)
    except Exception as e:
        current_app.logger.error(f'Error in get_student_coops: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Get dashboard metrics
@student.route('/metrics/<int:user_id>', methods=['GET'])
def get_student_metrics(user_id):
    try:
        cursor = db.get_db().cursor()
        
        # Get active applications count
        cursor.execute('''
            SELECT COUNT(*) as active_applications
            FROM application
            WHERE user_id = %s AND status = 'Pending'
        ''', (user_id,))
        active_apps = cursor.fetchone()['active_applications']
        
        # Get resume count
        cursor.execute('''
            SELECT COUNT(*) as resume_versions
            FROM resume
            WHERE user_id = %s
        ''', (user_id,))
        resume_count = cursor.fetchone()['resume_versions']
        
        # Get latest co-op
        cursor.execute('''
            SELECT company_name, end_date
            FROM co_op_record
            WHERE student_id = %s
            ORDER BY end_date DESC
            LIMIT 1
        ''', (user_id,))
        latest_coop = cursor.fetchone()
        
        metrics = {
            'active_applications': active_apps,
            'resume_versions': resume_count,
            'latest_coop': f"{latest_coop['company_name']} ({latest_coop['end_date'].year})" if latest_coop else "None"
        }
        
        return make_response(jsonify(metrics), 200)
    except Exception as e:
        current_app.logger.error(f'Error in get_student_metrics: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Get resume details
@student.route('/resume/<int:resume_id>', methods=['GET'])
def get_resume_details(resume_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT r.*, s.full_name, s.email
            FROM resume r
            JOIN student s ON r.user_id = s.user_id
            WHERE r.resume_id = %s
        ''', (resume_id,))
        resume = cursor.fetchone()
        
        if not resume:
            return make_response(jsonify({'error': 'Resume not found'}), 404)
            
        return make_response(jsonify(resume), 200)
    except Exception as e:
        current_app.logger.error(f'Error in get_resume_details: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Update resume content
@student.route('/resume/<int:resume_id>', methods=['PUT'])
def update_resume(resume_id):
    try:
        resume_data = request.json
        cursor = db.get_db().cursor()
        
        query = '''UPDATE resume 
                  SET education = %s,
                      skills = %s,
                      projects = %s,
                      co_op = %s
                  WHERE resume_id = %s'''
        data = (
            resume_data['education'],
            resume_data['skills'],
            resume_data['projects'],
            resume_data['co_op'],
            resume_id
        )
        
        cursor.execute(query, data)
        db.get_db().commit()
        
        if cursor.rowcount == 0:
            return make_response(jsonify({'error': 'Resume not found'}), 404)
            
        return make_response(jsonify({'message': 'Resume updated successfully'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error in update_resume: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)