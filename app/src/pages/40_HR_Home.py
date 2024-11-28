from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

hr_bp = Blueprint('hr', __name__)

# Get all internship postings
@hr_bp.route('/internships', methods=['GET'])
def get_internships():
    current_app.logger.info('GET /hr/internships route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT post_id, title, description, posted_by FROM internship_posting')
    the_data = cursor.fetchall()
    the_response = make_response(jsonify(the_data))
    the_response.status_code = 200
    return the_response

# Add a new internship posting
@hr_bp.route('/internships', methods=['POST'])
def add_internship():
    current_app.logger.info('POST /hr/internships route')
    posting_info = request.json
    query = '''INSERT INTO internship_posting (title, description, posted_by)
               VALUES (%s, %s, %s)'''
    data = (posting_info['title'], posting_info['description'], posting_info['posted_by'])
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    return make_response(jsonify({'message': 'Internship posting added!'}), 201)

# Update an internship posting
@hr_bp.route('/internships/<int:post_id>', methods=['PUT'])
def update_internship(post_id):
    current_app.logger.info(f'PUT /hr/internships/{post_id} route')
    posting_info = request.json
    query = '''UPDATE internship_posting SET title = %s, description = %s
               WHERE post_id = %s'''
    data = (posting_info['title'], posting_info['description'], post_id)
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    return jsonify({'message': f'Internship posting ID {post_id} updated!'})

# Delete an internship posting
@hr_bp.route('/internships/<int:post_id>', methods=['DELETE'])
def delete_internship(post_id):
    current_app.logger.info(f'DELETE /hr/internships/{post_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM internship_posting
