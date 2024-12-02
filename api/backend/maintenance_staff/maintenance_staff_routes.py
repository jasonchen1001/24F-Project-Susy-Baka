from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db
import logging
from datetime import datetime

maintenance = Blueprint('maintenance', __name__)
logger = logging.getLogger(__name__)

def serialize_results(cursor, rows):
    """Convert database rows to dictionaries with column names"""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in rows]

def get_or_create_database_info(cursor, name='project_susy_baka', version='1.0', db_type='MySQL', staff_id=1):
    """Get existing database info or create new one"""
    cursor.execute('''
        SELECT database_id FROM database_info 
        WHERE name = %s AND version = %s
        LIMIT 1
    ''', (name, version))
    result = cursor.fetchone()
    
    if result:
        return result[0]
    
    cursor.execute('''
        INSERT INTO database_info 
        (staff_id, name, version, type, last_update) 
        VALUES (%s, %s, %s, %s, CURRENT_DATE)
    ''', (staff_id, name, version, db_type))
    
    return cursor.lastrowid

@maintenance.route('/alerts', methods=['GET'])
def get_alerts():
    """Get alert history with database details"""
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT 
                ah.metrics,
                ah.alerts,
                ah.severity,
                di.name as database_name,
                di.version as db_version,
                di.type as db_type,
                ms.full_name as staff_name,
                di.database_id
            FROM alert_history ah
            JOIN database_info di ON ah.database_id = di.database_id
            JOIN maintenance_staff ms ON di.staff_id = ms.staff_id
            ORDER BY ah.severity DESC
        ''')
        alerts = serialize_results(cursor, cursor.fetchall())
        return make_response(jsonify(alerts), 200)
    except Exception as e:
        current_app.logger.error(f'Error in get_alerts: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

@maintenance.route('/alerts', methods=['PUT'])
def update_alert():
    """Update alert parameters"""
    try:
        cursor = db.get_db().cursor()
        alert_data = request.json
        
        query = '''UPDATE alert_history 
                  SET metrics = %s, alerts = %s, severity = %s
                  WHERE database_id = %s'''
        cursor.execute(query, (
            alert_data['metrics'],
            alert_data['alerts'],
            alert_data['severity'],
            alert_data['database_id']
        ))
        
        db.get_db().commit()
        return make_response(jsonify({'message': 'Alert updated successfully'}), 200)
    except Exception as e:
        db.get_db().rollback()
        current_app.logger.error(f'Error in update_alert: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

@maintenance.route('/backups', methods=['GET'])
def get_backup_history():
    """Get backup history with database details"""
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT 
                bh.type,
                bh.backup_date,
                bh.backup_type,
                bh.details,
                di.name AS database_name,
                di.version AS db_version,
                ms.full_name AS staff_name,
                di.database_id
            FROM backup_history bh
            JOIN database_info di ON bh.database_id = di.database_id
            JOIN maintenance_staff ms ON di.staff_id = ms.staff_id
            ORDER BY bh.backup_date DESC
        ''')
        backups = serialize_results(cursor, cursor.fetchall())
        return make_response(jsonify(backups), 200)
    except Exception as e:
        current_app.logger.error(f"Error in get_backup_history: {str(e)}")
        return make_response(jsonify({'error': f"Internal Server Error: {str(e)}"}), 500)

@maintenance.route('/backups', methods=['POST'])
def create_backup():
    """Create new backup record"""
    try:
        cursor = db.get_db().cursor()
        backup_data = request.json
        
        # Get or create database info entry
        database_id = get_or_create_database_info(cursor)
        
        # Create backup record
        cursor.execute('''
            INSERT INTO backup_history 
            (type, backup_date, backup_type, details, database_id)
            VALUES (%s, CURRENT_DATE, %s, %s, %s)
        ''', (
            backup_data.get('type', 'Full'),
            backup_data.get('schedule', 'Manual'),
            backup_data.get('description', 'Manual backup'),
            database_id
        ))
        
        db.get_db().commit()
        return make_response(jsonify({
            'message': 'Backup created successfully',
            'database_id': database_id
        }), 201)
    except Exception as e:
        db.get_db().rollback()
        current_app.logger.error(f'Error in create_backup: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

@maintenance.route('/alterations', methods=['GET'])
def get_alterations():
    """Get data alteration history"""
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT 
                dah.alteration_type,
                dah.alteration_date,
                di.name as database_name,
                di.version as db_version,
                ms.full_name as staff_name,
                di.database_id
            FROM data_alteration_history dah
            JOIN database_info di ON dah.database_id = di.database_id
            JOIN maintenance_staff ms ON di.staff_id = ms.staff_id
            ORDER BY dah.alteration_date DESC
        ''')
        alterations = serialize_results(cursor, cursor.fetchall())
        return make_response(jsonify(alterations), 200)
    except Exception as e:
        current_app.logger.error(f'Error in get_alterations: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

@maintenance.route('/alterations', methods=['POST'])
def create_alteration():
    """Create new alteration record"""
    try:
        cursor = db.get_db().cursor()
        alteration_data = request.json
        
        # Get or create database info entry
        database_id = get_or_create_database_info(cursor)
        
        # Create alteration record
        cursor.execute('''
            INSERT INTO data_alteration_history 
            (alteration_type, alteration_date, database_id)
            VALUES (%s, CURRENT_DATE, %s)
        ''', (
            alteration_data.get('alteration_type'),
            database_id
        ))
        
        db.get_db().commit()
        return make_response(jsonify({
            'message': 'Alteration created successfully',
            'database_id': database_id
        }), 201)
    except Exception as e:
        db.get_db().rollback()
        current_app.logger.error(f'Error in create_alteration: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

@maintenance.route('/databases', methods=['GET'])
def get_databases():
    """Get all database information"""
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT DISTINCT
                di.database_id,
                di.name,
                di.version,
                di.type,
                di.last_update,
                ms.full_name as staff_name,
                COUNT(DISTINCT ah.database_id) as alert_count,
                COUNT(DISTINCT dah.database_id) as alteration_count
            FROM database_info di
            JOIN maintenance_staff ms ON di.staff_id = ms.staff_id
            LEFT JOIN alert_history ah ON di.database_id = ah.database_id
            LEFT JOIN data_alteration_history dah ON di.database_id = dah.database_id
            GROUP BY di.database_id, di.name, di.version, di.type, di.last_update, ms.full_name
            ORDER BY di.last_update DESC
        ''')
        databases = serialize_results(cursor, cursor.fetchall())
        return make_response(jsonify(databases), 200)
    except Exception as e:
        current_app.logger.error(f'Error in get_databases: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)