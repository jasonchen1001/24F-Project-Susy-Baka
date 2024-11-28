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
@student.route('/<int:user_id>/grades', methods=['GET'])
def get_student_grades(user_id):
    """Get student academic records"""
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT g.course_name, g.grade, g.recorded_date, sa.full_name AS recorded_by
            FROM grade_record g
            JOIN school_admin sa ON g.recorded_by = sa.admin_id
            WHERE g.student_id = %s
            ORDER BY g.recorded_date DESC
        ''', (user_id,))
        grades = cursor.fetchall()

        if not grades:
            return make_response(jsonify({'message': 'No academic records found for the student'}), 404)

        return make_response(jsonify(grades), 200)
    except Exception as e:
        current_app.logger.error(f"Error in get_student_grades: {str(e)}")
        return make_response(jsonify({'error': str(e)}), 500)


#------------------------------------------------------------
# Get student co-op records
@student.route('/<int:user_id>/coops', methods=['GET'])
def get_coop_history(user_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT co_op_id, company_name, start_date, end_date, 
                   (SELECT full_name FROM school_admin WHERE admin_id = co_op_record.approved_by) AS approved_by
            FROM co_op_record
            WHERE student_id = %s
            ORDER BY start_date DESC
        ''', (user_id,))
        coops = cursor.fetchall()

        if not coops:
            return make_response(jsonify([]), 200)
        return make_response(jsonify(coops), 200)
    except Exception as e:
        current_app.logger.error(f"Error in get_coop_history: {str(e)}")
        return make_response(jsonify({'error': str(e)}), 500)


#------------------------------------------------------------
# Get dashboard metrics
@student.route('/<int:user_id>/metrics', methods=['GET'])
def get_student_metrics(user_id):
    """Fetch student metrics for dashboard"""
    try:
        cursor = db.get_db().cursor()

        # Query for active applications
        cursor.execute('''
            SELECT COUNT(*) AS active_applications
            FROM application 
            WHERE user_id = %s AND status = 'Pending'
        ''', (user_id,))
        active_applications_result = cursor.fetchone()
        

        # Query for resume versions
        cursor.execute('''
            SELECT COUNT(*) AS resume_versions
            FROM resume 
            WHERE user_id = %s
        ''', (user_id,))
        resume_versions_result = cursor.fetchone()

        # Query for latest co-op experience
        cursor.execute('''
            SELECT company_name AS latest_coop
            FROM co_op_record 
            WHERE student_id = %s 
            ORDER BY end_date DESC 
            LIMIT 1
        ''', (user_id,))
        latest_coop_result = cursor.fetchone()
       

        # Combine results
        metrics = {
            "active_applications": active_applications_result,
            "resume_versions": resume_versions_result,
            "latest_coop": latest_coop_result
        }

        current_app.logger.info(f"Metrics for user {user_id}: {metrics}")

        return make_response(jsonify(metrics), 200)
    except Exception as e:
        current_app.logger.error(f"Error fetching metrics for user {user_id}: {str(e)}")
        return make_response(jsonify({"error": str(e)}), 500)



#------------------------------------------------------------
# Get resume details
@student.route('/<int:user_id>/resume', methods=['GET'])
def get_current_resume(user_id):
    """Get the current resume of a student"""
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT r.*, s.full_name, s.email
            FROM resume r
            JOIN student s ON r.user_id = s.user_id
            WHERE r.user_id = %s
            ORDER BY r.time_uploaded DESC
            LIMIT 1
        ''', (user_id,))
        resume = cursor.fetchone()

        if not resume:
            return make_response(jsonify({'message': 'No resume found for this student'}), 404)

        return make_response(jsonify(resume), 200)
    except Exception as e:
        current_app.logger.error(f"Error in get_current_resume: {str(e)}")
        return make_response(jsonify({'error': str(e)}), 500)


#------------------------------------------------------------
# Update resume content
@student.route('/<int:user_id>/resume', methods=['PUT'])
def update_resume(user_id):
    """Update the resume of a student"""
    try:
        resume_data = request.json
        cursor = db.get_db().cursor()
        
        cursor.execute('''
            UPDATE resume
            SET doc_name = %s, education = %s, skills = %s, projects = %s, co_op = %s
            WHERE user_id = %s
        ''', (
            resume_data.get('doc_name'),
            resume_data.get('education'),
            resume_data.get('skills'),
            resume_data.get('projects'),
            resume_data.get('co_op'),
            user_id
        ))
        db.get_db().commit()

        if cursor.rowcount == 0:
            return make_response(jsonify({'message': 'Resume not found'}), 404)

        return make_response(jsonify({'message': 'Resume updated successfully'}), 200)
    except Exception as e:
        current_app.logger.error(f"Error in update_resume: {str(e)}")
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# View resume suggestions
@student.route('/<int:user_id>/resume/suggestions', methods=['GET'])
def get_resume_suggestions(user_id):
    """Get suggestions for the current resume of a student"""
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT s.suggestion_id, s.suggestion_text, s.time_created
            FROM suggestion s
            JOIN resume r ON s.resume_id = r.resume_id
            WHERE r.user_id = %s
            ORDER BY s.time_created DESC
        ''', (user_id,))
        suggestions = cursor.fetchall()

        if not suggestions:
            return make_response(jsonify({'message': 'No suggestions found for this resume'}), 404)

        return make_response(jsonify(suggestions), 200)
    except Exception as e:
        current_app.logger.error(f"Error in get_resume_suggestions: {str(e)}")
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Get active applications for a student
@student.route('/<int:user_id>/applications/active', methods=['GET'])
def get_active_applications(user_id):
    """Get active internship applications for a student"""
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT 
                a.application_id,
                i.title AS position_title,
                i.description AS position_description,
                i.requirements,
                h.company_name,
                a.status,
                a.sent_on
            FROM application a
            JOIN internship_position i ON a.position_id = i.position_id
            JOIN hr_manager h ON i.hr_id = h.hr_id
            WHERE a.user_id = %s AND a.status = 'Pending'
            ORDER BY a.sent_on DESC
        ''', (user_id,))
        
        active_applications = cursor.fetchall()
        if not active_applications:
            return make_response(jsonify({'message': 'No active applications found.'}), 404)

        return make_response(jsonify(active_applications), 200)
    except Exception as e:
        current_app.logger.error(f"Error fetching active applications: {str(e)}")
        return make_response(jsonify({'error': str(e)}), 500)




#------------------------------------------------------------
# View application history
@student.route('/<int:user_id>/applications/history', methods=['GET'])
def get_application_history(user_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT 
                a.application_id,
                i.title AS position_title,
                i.description AS position_description,
                i.requirements,
                h.company_name,
                a.status,
                a.sent_on
            FROM application a
            JOIN internship_position i ON a.position_id = i.position_id
            JOIN hr_manager h ON i.hr_id = h.hr_id
            WHERE a.user_id = %s AND a.status != 'Pending'
            ORDER BY a.sent_on DESC
        ''', (user_id,))
        application_history = cursor.fetchall()

        # Debugging output to check data
        current_app.logger.info(f"Application History Data: {application_history}")

        if not application_history:
            return make_response(jsonify([]), 200)

        return make_response(jsonify(application_history), 200)
    except Exception as e:
        current_app.logger.error(f"Error fetching application history: {str(e)}")
        return make_response(jsonify({'error': str(e)}), 500)


#------------------------------------------------------------
# Get available positions for a student
@student.route('/<int:user_id>/applications/positions', methods=['GET'])
def get_available_positions(user_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT 
                i.position_id,
                i.title AS position_title,
                i.description AS position_description,
                i.requirements,
                h.company_name,
                i.posted_date,
                i.status
            FROM internship_position i
            JOIN hr_manager h ON i.hr_id = h.hr_id
            WHERE i.status = 'Active'
            ORDER BY i.posted_date DESC
        ''')
        
        result = cursor.fetchall()
        if not result:
            return make_response(jsonify({'message': 'No available positions found'}), 404)

        return make_response(jsonify(result), 200)
    except Exception as e:
        current_app.logger.error(f"Error fetching available positions: {str(e)}")
        return make_response(jsonify({'error': str(e)}), 500)
