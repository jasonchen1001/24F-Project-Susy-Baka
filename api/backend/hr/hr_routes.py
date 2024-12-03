from flask import Blueprint, request, jsonify, make_response
from backend.db_connection import db
import logging
from datetime import datetime

hr_bp = Blueprint('hr', __name__)
logger = logging.getLogger(__name__)

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
            GROUP BY ip.position_id, ip.title, ip.description, ip.requirements, 
                     ip.status, ip.posted_date, ip.hr_id
        ''')
        positions = cursor.fetchall()
        return make_response(jsonify(positions), 200)
    except Exception as e:
        logger.error(f"Error getting internships: {str(e)}")
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
        logger.error(f"Error adding internship: {str(e)}")
        return make_response(jsonify({'error': str(e)}), 500)

@hr_bp.route('/internships/<int:position_id>', methods=['DELETE'])
def delete_internship(position_id):
    """Delete an internship position"""
    try:
        cursor = db.get_db().cursor()
        
        # Check if position exists and belongs to the HR manager
        cursor.execute('''
            SELECT COUNT(*) as count 
            FROM internship_position 
            WHERE position_id = %s
        ''', (position_id,))
        result = cursor.fetchone()
        
        if not result or result['count'] == 0:
            logger.error(f"Position {position_id} not found")
            return make_response(jsonify({'error': 'Position not found'}), 404)
        
        # Check for existing applications
        cursor.execute('''
            SELECT COUNT(*) as app_count 
            FROM application 
            WHERE position_id = %s
        ''', (position_id,))
        app_result = cursor.fetchone()
        
        # If there are applications, perform soft delete by updating status
        if app_result['app_count'] > 0:
            logger.info(f"Position {position_id} has applications, performing soft delete")
            cursor.execute('''
                UPDATE internship_position 
                SET status = 'Inactive'
                WHERE position_id = %s
            ''', (position_id,))
            db.get_db().commit()
            return make_response(jsonify({
                'message': 'Position deactivated due to existing applications'
            }), 200)
        
        # If no applications, perform hard delete
        cursor.execute('''
            DELETE FROM internship_position 
            WHERE position_id = %s
        ''', (position_id,))
        db.get_db().commit()
        
        logger.info(f"Position {position_id} deleted successfully")
        return make_response(jsonify({'message': 'Position deleted successfully'}), 200)
    
    except Exception as e:
        db.get_db().rollback()
        logger.error(f"Error deleting position {position_id}: {str(e)}")
        return make_response(jsonify({'error': str(e)}), 500)

# Application Management Routes
@hr_bp.route('/applications', methods=['GET'])
def get_applications():
    """Get applications with optional status filter"""
    try:
        status = request.args.get('status')
        cursor = db.get_db().cursor()
        
        if status and status != "all":
            query = '''
                WITH RankedApplications AS (
                    SELECT a.*,
                           ROW_NUMBER() OVER (PARTITION BY a.user_id, a.position_id 
                                            ORDER BY a.sent_on DESC) as rn
                    FROM application a
                    WHERE a.status = %s
                )
                SELECT DISTINCT ra.*, s.full_name, s.email, ip.title as position_title
                FROM RankedApplications ra
                JOIN student s ON ra.user_id = s.user_id
                JOIN internship_position ip ON ra.position_id = ip.position_id
                WHERE ra.rn = 1
            '''
            cursor.execute(query, (status,))
        else:
            query = '''
                WITH RankedApplications AS (
                    SELECT a.*,
                           ROW_NUMBER() OVER (PARTITION BY a.user_id, a.position_id 
                                            ORDER BY a.sent_on DESC) as rn
                    FROM application a
                )
                SELECT DISTINCT ra.*, s.full_name, s.email, ip.title as position_title
                FROM RankedApplications ra
                JOIN student s ON ra.user_id = s.user_id
                JOIN internship_position ip ON ra.position_id = ip.position_id
                WHERE ra.rn = 1
            '''
            cursor.execute(query)
            
        applications = cursor.fetchall()
        return make_response(jsonify(applications), 200)
    except Exception as e:
        logger.error(f"Error getting applications: {str(e)}")
        return make_response(jsonify({'error': str(e)}), 500)

@hr_bp.route('/applications/<int:application_id>', methods=['PUT'])
def update_application_status(application_id):
    """Update application status"""
    try:
        status = request.json['status']
        logger.info(f"Updating application {application_id} to status: {status}")
        
        cursor = db.get_db().cursor()
        cursor.execute('''
            UPDATE application 
            SET status = %s,
                sent_on = CURRENT_TIMESTAMP
            WHERE application_id = %s
        ''', (status, application_id))
        db.get_db().commit()
        
        # Verify update
        cursor.execute('''
            SELECT a.*, s.full_name, ip.title as position_title
            FROM application a
            JOIN student s ON a.user_id = s.user_id
            JOIN internship_position ip ON a.position_id = ip.position_id
            WHERE a.application_id = %s
        ''', (application_id,))
        
        result = cursor.fetchone()
        if result:
            logger.info(f"Successfully updated application {application_id} to {status}")
            return make_response(jsonify({
                'message': 'Application status updated',
                'application': result
            }), 200)
        else:
            logger.error(f"Application {application_id} not found after update")
            return make_response(jsonify({'error': 'Application not found'}), 404)
    except Exception as e:
        db.get_db().rollback()
        logger.error(f"Error updating application: {str(e)}")
        return make_response(jsonify({'error': str(e)}), 500)

@hr_bp.route('/applications/<int:application_id>', methods=['DELETE'])
def delete_application(application_id):
    """Delete an application"""
    try:
        cursor = db.get_db().cursor()
        
        # Check if application exists
        cursor.execute('''
            SELECT status 
            FROM application 
            WHERE application_id = %s
        ''', (application_id,))
        result = cursor.fetchone()
        
        if not result:
            logger.error(f"Application {application_id} not found")
            return make_response(jsonify({'error': 'Application not found'}), 404)
        
        # Don't allow deletion of processed applications
        if result['status'] in ['Accepted', 'Rejected']:
            logger.error(f"Cannot delete processed application {application_id}")
            return make_response(jsonify({
                'error': 'Cannot delete processed applications'
            }), 400)
        
        cursor.execute('''
            DELETE FROM application 
            WHERE application_id = %s
        ''', (application_id,))
        db.get_db().commit()
        
        logger.info(f"Application {application_id} deleted successfully")
        return make_response(jsonify({'message': 'Application deleted successfully'}), 200)
    
    except Exception as e:
        db.get_db().rollback()
        logger.error(f"Error deleting application {application_id}: {str(e)}")
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
        logger.error(f"Error getting resumes: {str(e)}")
        return make_response(jsonify({'error': str(e)}), 500)

@hr_bp.route('/resumes/<int:resume_id>/suggestions/<int:suggestion_id>', methods=['DELETE'])
def delete_suggestion(resume_id, suggestion_id):
    """Delete a resume suggestion"""
    try:
        cursor = db.get_db().cursor()
        
        # Check if suggestion exists and belongs to the resume
        cursor.execute('''
            SELECT COUNT(*) as count 
            FROM suggestion 
            WHERE suggestion_id = %s AND resume_id = %s
        ''', (suggestion_id, resume_id))
        result = cursor.fetchone()
        
        if not result or result['count'] == 0:
            logger.error(f"Suggestion {suggestion_id} not found for resume {resume_id}")
            return make_response(jsonify({'error': 'Suggestion not found'}), 404)
        
        cursor.execute('''
            DELETE FROM suggestion 
            WHERE suggestion_id = %s
        ''', (suggestion_id,))
        db.get_db().commit()
        
        logger.info(f"Suggestion {suggestion_id} deleted successfully")
        return make_response(jsonify({'message': 'Suggestion deleted successfully'}), 200)
    
    except Exception as e:
        db.get_db().rollback()
        logger.error(f"Error deleting suggestion {suggestion_id}: {str(e)}")
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
            GROUP BY ip.position_id, ip.title
        ''')
        analytics = cursor.fetchall()
        return make_response(jsonify(analytics), 200)
    except Exception as e:
        logger.error(f"Error getting analytics: {str(e)}")
        return make_response(jsonify({'error': str(e)}), 500)
    
