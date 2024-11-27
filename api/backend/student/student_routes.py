from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

student = Blueprint('student', __name__)

#------------------------------------------------------------
# Get list of all student resumes (Story 1)
@student.route('/resumes', methods=['GET'])
def get_all_resumes():
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT r.resume_id, r.user_id, r.time_uploaded, r.doc_name,
                   s.full_name, s.email
            FROM resume r
            JOIN student s ON r.user_id = s.user_id
            ORDER BY r.time_uploaded DESC
        ''')
        resumes = cursor.fetchall()
        return make_response(jsonify(resumes), 200)
    except Exception as e:
        current_app.logger.error(f'Error in get_all_resumes: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Upload new resume (Story 1)
@student.route('/resumes', methods=['POST'])
def upload_resume():
    try:
        resume_data = request.json
        cursor = db.get_db().cursor()
        
        query = '''INSERT INTO resume 
                  (resume_id, user_id, doc_name) 
                  VALUES (%s, %s, %s)'''
        data = (resume_data['resume_id'], resume_data['user_id'], resume_data['doc_name'])
        
        cursor.execute(query, data)
        db.get_db().commit()
        
        return make_response(jsonify({'message': 'Resume uploaded successfully'}), 201)
    except Exception as e:
        current_app.logger.error(f'Error in upload_resume: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Get specific resume details (Story 5)
@student.route('/resumes/<resume_id>', methods=['GET'])
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
# Update resume content (Story 5)
@student.route('/resumes/<resume_id>', methods=['PUT'])
def update_resume(resume_id):
    try:
        resume_data = request.json
        cursor = db.get_db().cursor()
        
        query = '''UPDATE resume 
                  SET doc_name = %s
                  WHERE resume_id = %s'''
        data = (resume_data['doc_name'], resume_id)
        
        cursor.execute(query, data)
        db.get_db().commit()
        
        if cursor.rowcount == 0:
            return make_response(jsonify({'error': 'Resume not found'}), 404)
            
        return make_response(jsonify({'message': 'Resume updated successfully'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error in update_resume: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Delete specific resume (Story 5)
@student.route('/resumes/<resume_id>', methods=['DELETE'])
def delete_resume(resume_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('DELETE FROM resume WHERE resume_id = %s', (resume_id,))
        db.get_db().commit()
        
        if cursor.rowcount == 0:
            return make_response(jsonify({'error': 'Resume not found'}), 404)
            
        return make_response(jsonify({'message': 'Resume deleted successfully'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error in delete_resume: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Get application history (Story 3)
@student.route('/applications', methods=['GET'])
def get_applications():
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT a.*, i.title, i.description
            FROM application a
            JOIN internship_position i ON a.position_id = i.position_id
            ORDER BY a.sent_on DESC
        ''')
        applications = cursor.fetchall()
        return make_response(jsonify(applications), 200)
    except Exception as e:
        current_app.logger.error(f'Error in get_applications: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Submit new application (Story 3)
@student.route('/applications', methods=['POST'])
def submit_application():
    try:
        app_data = request.json
        cursor = db.get_db().cursor()
        
        query = '''INSERT INTO application 
                  (application_id, user_id, position_id, sent_on, status) 
                  VALUES (%s, %s, %s, CURRENT_DATE, 'Pending')'''
        data = (app_data['application_id'], app_data['user_id'], app_data['position_id'])
        
        cursor.execute(query, data)
        db.get_db().commit()
        
        return make_response(jsonify({'message': 'Application submitted successfully'}), 201)
    except Exception as e:
        current_app.logger.error(f'Error in submit_application: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Get specific application status (Story 3)
@student.route('/applications/<application_id>', methods=['GET'])
def get_application_status(application_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT a.*, i.title, i.description
            FROM application a
            JOIN internship_position i ON a.position_id = i.position_id
            WHERE a.application_id = %s
        ''', (application_id,))
        
        application = cursor.fetchone()
        if not application:
            return make_response(jsonify({'error': 'Application not found'}), 404)
            
        return make_response(jsonify(application), 200)
    except Exception as e:
        current_app.logger.error(f'Error in get_application_status: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Update application status (Story 3)
@student.route('/applications/<application_id>', methods=['PUT'])
def update_application(application_id):
    try:
        app_data = request.json
        cursor = db.get_db().cursor()
        
        if app_data['status'] not in ['Pending', 'Accepted', 'Rejected']:
            return make_response(jsonify({'error': 'Invalid status'}), 400)
        
        query = '''UPDATE application 
                  SET status = %s
                  WHERE application_id = %s'''
        data = (app_data['status'], application_id)
        
        cursor.execute(query, data)
        db.get_db().commit()
        
        if cursor.rowcount == 0:
            return make_response(jsonify({'error': 'Application not found'}), 404)
            
        return make_response(jsonify({'message': 'Application status updated successfully'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error in update_application: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Cancel application (Story 3)
@student.route('/applications/<application_id>', methods=['DELETE'])
def cancel_application(application_id):
    try:
        cursor = db.get_db().cursor()
        
        # First check if the application exists and can be cancelled
        cursor.execute('SELECT status FROM application WHERE application_id = %s', (application_id,))
        application = cursor.fetchone()
        
        if not application:
            return make_response(jsonify({'error': 'Application not found'}), 404)
            
        if application['status'] not in ['Pending']:
            return make_response(jsonify({'error': 'Cannot cancel application in current status'}), 400)
        
        # Delete the application
        cursor.execute('DELETE FROM application WHERE application_id = %s', (application_id,))
        db.get_db().commit()
        
        return make_response(jsonify({'message': 'Application cancelled successfully'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error in cancel_application: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Get notification list (Story 4)
@student.route('/notifications', methods=['GET'])
def get_notifications():
    try:
        cursor = db.get_db().cursor()
        # 假设我们有一个notifications表
        cursor.execute('''
            SELECT s.suggestion_id, s.suggestion_text, s.time_created,
                   r.doc_name, r.resume_id
            FROM suggestion s
            JOIN resume r ON s.resume_id = r.resume_id
            ORDER BY s.time_created DESC
        ''')
        notifications = cursor.fetchall()
        return make_response(jsonify(notifications), 200)
    except Exception as e:
        current_app.logger.error(f'Error in get_notifications: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Mark notification as read (Story 4)
@student.route('/notifications/<suggestion_id>', methods=['PUT'])
def mark_notification_read(suggestion_id):
    try:
        cursor = db.get_db().cursor()
        query = '''UPDATE suggestion 
                  SET suggestion_text = CONCAT(suggestion_text, ' (Read)')
                  WHERE suggestion_id = %s'''
        
        cursor.execute(query, (suggestion_id,))
        db.get_db().commit()
        
        if cursor.rowcount == 0:
            return make_response(jsonify({'error': 'Notification not found'}), 404)
            
        return make_response(jsonify({'message': 'Notification marked as read'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error in mark_notification_read: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Delete notification (Story 4)
@student.route('/notifications/<suggestion_id>', methods=['DELETE'])
def delete_notification(suggestion_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('DELETE FROM suggestion WHERE suggestion_id = %s', (suggestion_id,))
        db.get_db().commit()
        
        if cursor.rowcount == 0:
            return make_response(jsonify({'error': 'Notification not found'}), 404)
            
        return make_response(jsonify({'message': 'Notification deleted successfully'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error in delete_notification: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)