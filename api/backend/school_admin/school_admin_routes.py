########################################################
# School Administrator blueprint
########################################################
from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

admin = Blueprint('admin', __name__)

#------------------------------------------------------------
# Get list of all students (Story 1)
@admin.route('/students', methods=['GET'])
def get_students():
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT s.*, u.dob, u.gender
            FROM student s
            JOIN user u ON s.user_id = u.user_id
        ''')
        students = cursor.fetchall()
        return make_response(jsonify(students), 200)
    except Exception as e:
        current_app.logger.error(f'Error in get_students: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Add new student record (Story 1)
@admin.route('/students', methods=['POST'])
def add_student():
    try:
        student_data = request.json
        cursor = db.get_db().cursor()
        
        # First insert into user table
        user_query = '''INSERT INTO user 
                       (full_name, email, role, dob, gender)
                       VALUES (%s, %s, 'Student', %s, %s)'''
        user_data = (student_data['full_name'], student_data['email'], 
                    student_data.get('dob'), student_data.get('gender'))
        
        cursor.execute(user_query, user_data)
        user_id = cursor.lastrowid
        
        # Then insert into student table
        student_query = '''INSERT INTO student 
                          (user_id, full_name, email)
                          VALUES (%s, %s, %s)'''
        student_data = (user_id, student_data['full_name'], student_data['email'])
        
        cursor.execute(student_query, student_data)
        db.get_db().commit()
        
        return make_response(jsonify({
            'message': 'Student added successfully',
            'user_id': user_id
        }), 201)
    except Exception as e:
        current_app.logger.error(f'Error in add_student: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Get specific student info (Story 1)
@admin.route('/students/<user_id>', methods=['GET'])
def get_student(user_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT s.*, u.dob, u.gender, 
                   gr.course_name, gr.grade
            FROM student s
            JOIN user u ON s.user_id = u.user_id
            LEFT JOIN grade_record gr ON s.user_id = gr.student_id
            WHERE s.user_id = %s
        ''', (user_id,))
        student = cursor.fetchall()
        
        if not student:
            return make_response(jsonify({'error': 'Student not found'}), 404)
            
        return make_response(jsonify(student), 200)
    except Exception as e:
        current_app.logger.error(f'Error in get_student: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Update student info (Story 2)
@admin.route('/students/<user_id>', methods=['PUT'])
def update_student(user_id):
    try:
        student_data = request.json
        cursor = db.get_db().cursor()
        
        # Update user table
        user_query = '''UPDATE user 
                       SET full_name = %s, email = %s, dob = %s, gender = %s
                       WHERE user_id = %s'''
        user_data = (student_data['full_name'], student_data['email'],
                    student_data.get('dob'), student_data.get('gender'), user_id)
        
        cursor.execute(user_query, user_data)
        
        # Update student table
        student_query = '''UPDATE student
                          SET full_name = %s, email = %s
                          WHERE user_id = %s'''
        student_data = (student_data['full_name'], student_data['email'], user_id)
        
        cursor.execute(student_query, student_data)
        db.get_db().commit()
        
        if cursor.rowcount == 0:
            return make_response(jsonify({'error': 'Student not found'}), 404)
            
        return make_response(jsonify({'message': 'Student updated successfully'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error in update_student: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Delete student record (Story 4)
@admin.route('/students/<user_id>', methods=['DELETE'])
def delete_student(user_id):
    try:
        cursor = db.get_db().cursor()
        # Due to ON DELETE CASCADE, deleting from user table will delete from student table
        cursor.execute('DELETE FROM user WHERE user_id = %s', (user_id,))
        db.get_db().commit()
        
        if cursor.rowcount == 0:
            return make_response(jsonify({'error': 'Student not found'}), 404)
            
        return make_response(jsonify({'message': 'Student deleted successfully'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error in delete_student: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Get academic records (Story 1)
@admin.route('/academic-records', methods=['GET'])
def get_academic_records():
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT gr.*, s.full_name, s.email
            FROM grade_record gr
            JOIN student s ON gr.student_id = s.user_id
            ORDER BY gr.recorded_date DESC
        ''')
        records = cursor.fetchall()
        return make_response(jsonify(records), 200)
    except Exception as e:
        current_app.logger.error(f'Error in get_academic_records: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Create new academic record (Story 2)
@admin.route('/academic-records', methods=['POST'])
def create_academic_record():
    try:
        record_data = request.json
        cursor = db.get_db().cursor()
        
        query = '''INSERT INTO grade_record 
                  (student_id, course_name, grade, recorded_by)
                  VALUES (%s, %s, %s, %s)'''
        data = (record_data['student_id'], record_data['course_name'],
               record_data['grade'], record_data['recorded_by'])
        
        cursor.execute(query, data)
        db.get_db().commit()
        
        return make_response(jsonify({'message': 'Academic record created successfully'}), 201)
    except Exception as e:
        current_app.logger.error(f'Error in create_academic_record: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Get compliance reports (Story 3)
@admin.route('/reports', methods=['GET'])
def get_reports():
    try:
        cursor = db.get_db().cursor()
        # Get various compliance metrics
        cursor.execute('''
            SELECT 
                COUNT(DISTINCT s.user_id) as total_students,
                COUNT(DISTINCT cr.co_op_id) as total_coops,
                AVG(gr.grade) as avg_grade
            FROM student s
            LEFT JOIN grade_record gr ON s.user_id = gr.student_id
            LEFT JOIN co_op_record cr ON s.user_id = cr.student_id
        ''')
        reports = cursor.fetchall()
        return make_response(jsonify(reports), 200)
    except Exception as e:
        current_app.logger.error(f'Error in get_reports: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Generate new report (Story 3)
@admin.route('/reports', methods=['POST'])
def generate_report():
    try:
        report_data = request.json
        cursor = db.get_db().cursor()
        
        # Example: Generate detailed report based on specific criteria
        if report_data['type'] == 'grade_distribution':
            cursor.execute('''
                SELECT course_name, 
                       AVG(grade) as avg_grade,
                       MIN(grade) as min_grade,
                       MAX(grade) as max_grade,
                       COUNT(*) as total_students
                FROM grade_record
                GROUP BY course_name
            ''')
        elif report_data['type'] == 'coop_status':
            cursor.execute('''
                SELECT company_name,
                       COUNT(*) as student_count,
                       MIN(start_date) as earliest_start,
                       MAX(end_date) as latest_end
                FROM co_op_record
                GROUP BY company_name
            ''')
            
        report_results = cursor.fetchall()
        return make_response(jsonify(report_results), 200)
    except Exception as e:
        current_app.logger.error(f'Error in generate_report: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Delete old report (Story 4)
@admin.route('/reports/<report_id>', methods=['DELETE'])
def delete_report(report_id):
    # Implementation would depend on how reports are stored
    # This is a placeholder implementation
    try:
        return make_response(jsonify({'message': 'Report deleted successfully'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error in delete_report: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Get performance analytics (Story 6)
@admin.route('/analytics', methods=['GET'])
def get_analytics():
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT 
                course_name,
                COUNT(*) as student_count,
                AVG(grade) as avg_grade,
                COUNT(CASE WHEN grade >= 3.0 THEN 1 END) as high_performers
            FROM grade_record
            GROUP BY course_name
        ''')
        analytics = cursor.fetchall()
        return make_response(jsonify(analytics), 200)
    except Exception as e:
        current_app.logger.error(f'Error in get_analytics: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Update analytics parameters (Story 6)
@admin.route('/analytics', methods=['PUT'])
def update_analytics():
    try:
        analytics_data = request.json
        # Implementation would depend on how analytics parameters are stored
        return make_response(jsonify({'message': 'Analytics parameters updated successfully'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error in update_analytics: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)