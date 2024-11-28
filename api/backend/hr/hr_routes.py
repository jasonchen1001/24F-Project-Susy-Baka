from flask import Blueprint, request, jsonify, make_response
from backend.db_connection import db

hr_bp = Blueprint('hr', __name__)

# Position Management Routes
@hr_bp.route('/internships', methods=['GET'])
def get_internships():
    """Get all internship positions with application counts"""
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT ip.*, COUNT(a.application_id) as application_count
            FROM internship_position ip
            LEFT JOIN application a ON ip.position_id = a.position_id
            GROUP BY ip.position_id
        ''')
        positions = cursor.fetchall()
        return make_response(jsonify(positions), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

@hr_bp.route('/internships', methods=['POST'])
def add_internship():
    """Add a new internship position"""
    try:
        position_info = request.json
        query = '''INSERT INTO internship_position 
                   (hr_id, title, description, requirements, status, posted_date)
                   VALUES (%s, %s, %s, %s, %s, CURDATE())'''
        data = (
            position_info['hr_id'],
            position_info['title'],
            position_info['description'],
            position_info['requirements'],
            position_info['status']
        )
        cursor = db.get_db().cursor()
        cursor.execute(query, data)
        db.get_db().commit()
        return make_response(jsonify({'message': 'Position added successfully'}), 201)
    except Exception as e:
        db.get_db().rollback()
        return make_response(jsonify({'error': str(e)}), 500)

@hr_bp.route('/internships/<int:position_id>', methods=['PUT'])
def update_internship(position_id):
    """Update an existing internship position"""
    try:
        position_info = request.json
        query = '''UPDATE internship_position 
                   SET title = %s, description = %s, requirements = %s, status = %s
                   WHERE position_id = %s'''
        cursor = db.get_db().cursor()
        cursor.execute(query, (
            position_info['title'],
            position_info['description'],
            position_info['requirements'],
            position_info['status'],
            position_id
        ))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Position updated successfully'}), 200)
    except Exception as e:
        db.get_db().rollback()
        return make_response(jsonify({'error': str(e)}), 500)

@hr_bp.route('/internships/<int:position_id>', methods=['DELETE'])
def delete_internship(position_id):
    """Delete an internship position"""
    try:
        cursor = db.get_db().cursor()
        cursor.execute('DELETE FROM internship_position WHERE position_id = %s', (position_id,))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Position deleted successfully'}), 200)
    except Exception as e:
        db.get_db().rollback()
        return make_response(jsonify({'error': str(e)}), 500)

# Application Management Routes
@hr_bp.route('/applications', methods=['GET'])
def get_applications():
    """Get applications with optional status filter"""
    try:
        status = request.args.get('status', 'Pending')
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT a.*, s.full_name, s.email, ip.title as position_title
            FROM application a
            JOIN student s ON a.user_id = s.user_id
            JOIN internship_position ip ON a.position_id = ip.position_id
            WHERE a.status = %s
        ''', (status,))
        applications = cursor.fetchall()
        return make_response(jsonify(applications), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

@hr_bp.route('/applications/<int:application_id>', methods=['PUT'])
def update_application_status(application_id):
    """Update application status"""
    try:
        status = request.json['status']
        cursor = db.get_db().cursor()
        cursor.execute('''
            UPDATE application 
            SET status = %s 
            WHERE application_id = %s
        ''', (status, application_id))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Application status updated'}), 200)
    except Exception as e:
        db.get_db().rollback()
        return make_response(jsonify({'error': str(e)}), 500)

# Resume Management Routes
@hr_bp.route('/resumes', methods=['GET'])
def get_resumes():
    """Get all resumes with student information"""
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT r.*, s.full_name, s.email,
                   (SELECT suggestion_text 
                    FROM suggestion 
                    WHERE resume_id = r.resume_id 
                    ORDER BY time_created DESC 
                    LIMIT 1) as latest_suggestion
            FROM resume r
            JOIN student s ON r.user_id = s.user_id
            ORDER BY r.time_uploaded DESC
        ''')
        resumes = cursor.fetchall()
        return make_response(jsonify(resumes), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

@hr_bp.route('/resumes/<int:resume_id>/suggestions', methods=['POST'])
def add_resume_suggestion(resume_id):
    """Add a suggestion for a resume"""
    try:
        suggestion_text = request.json['suggestion_text']
        cursor = db.get_db().cursor()
        cursor.execute('''
            INSERT INTO suggestion (resume_id, suggestion_text)
            VALUES (%s, %s)
        ''', (resume_id, suggestion_text))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Suggestion added successfully'}), 201)
    except Exception as e:
        db.get_db().rollback()
        return make_response(jsonify({'error': str(e)}), 500)

# Analytics Routes
@hr_bp.route('/analytics/positions', methods=['GET'])
def get_position_analytics():
    """Get analytics for internship positions"""
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT 
                ip.position_id,
                ip.title,
                COUNT(a.application_id) as total_applications,
                SUM(CASE WHEN a.status = 'Accepted' THEN 1 ELSE 0 END) as accepted,
                SUM(CASE WHEN a.status = 'Rejected' THEN 1 ELSE 0 END) as rejected,
                SUM(CASE WHEN a.status = 'Pending' THEN 1 ELSE 0 END) as pending
            FROM internship_position ip
            LEFT JOIN application a ON ip.position_id = a.position_id
            GROUP BY ip.position_id
        ''')
        analytics = cursor.fetchall()
        return make_response(jsonify(analytics), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)