from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

maintenance = Blueprint('maintenance', __name__)

# Performance Monitoring Routes
@maintenance.route('/alerts', methods=['GET'])
def get_alerts():
    """Get alert history with database details"""
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT ah.database_id, ah.metrics, ah.alerts, ah.severity,
                   di.name as database_name, di.version, di.type,
                   ms.first_name, ms.last_name
            FROM alert_history ah
            JOIN database_info di ON ah.database_id = di.database_id
            JOIN maintenance_staff ms ON di.staff_id = ms.staff_id
            ORDER BY ah.severity DESC
        ''')
        alerts = cursor.fetchall()
        return make_response(jsonify(alerts), 200)
    except Exception as e:
        current_app.logger.error(f'Error in get_alerts: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

@maintenance.route('/alerts', methods=['PUT'])
def update_alert():
    """Update alert parameters"""
    try:
        alert_data = request.json
        cursor = db.get_db().cursor()
        
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

# Backup Management Routes
@maintenance.route('/backups', methods=['GET'])
def get_backup_history():
    """Get backup history with database details"""
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT bh.type, bh.backup_date, bh.backup_type, bh.details,
                   di.name as database_name, di.version,
                   ms.first_name, ms.last_name
            FROM backup_history bh
            JOIN database_info di ON bh.change_id = di.change_id
            JOIN maintenance_staff ms ON di.staff_id = ms.staff_id
            ORDER BY bh.backup_date DESC
        ''')
        backups = cursor.fetchall()
        return make_response(jsonify(backups), 200)
    except Exception as e:
        current_app.logger.error(f'Error in get_backup_history: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

@maintenance.route('/backups', methods=['POST'])
def create_backup():
    """Create new backup record"""
    try:
        backup_data = request.json
        cursor = db.get_db().cursor()
        
        query = '''INSERT INTO backup_history 
                  (type, backup_date, backup_type, details, change_id)
                  VALUES (%s, CURRENT_DATE, %s, %s, %s)'''
        cursor.execute(query, (
            backup_data['type'],
            backup_data['backup_type'],
            backup_data['details'],
            backup_data['change_id']
        ))
        db.get_db().commit()
        
        return make_response(jsonify({'message': 'Backup created successfully'}), 201)
    except Exception as e:
        db.get_db().rollback()
        current_app.logger.error(f'Error in create_backup: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

# Data Alteration Routes 
@maintenance.route('/alterations', methods=['GET'])
def get_alterations():
    """Get data alteration history"""
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT dah.alteration_type, dah.alteration_date,
                   di.name as database_name,
                   ms.first_name, ms.last_name
            FROM data_alteration_history dah
            JOIN database_info di ON dah.change_id = di.change_id
            JOIN maintenance_staff ms ON di.staff_id = ms.staff_id
            ORDER BY dah.alteration_date DESC
        ''')
        alterations = cursor.fetchall()
        return make_response(jsonify(alterations), 200)
    except Exception as e:
        current_app.logger.error(f'Error in get_alterations: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

@maintenance.route('/alterations', methods=['POST'])
def create_alteration():
    """Create new data alteration record"""
    try:
        alteration_data = request.json
        cursor = db.get_db().cursor()
        
        query = '''INSERT INTO data_alteration_history 
                  (alteration_type, alteration_date, change_id)
                  VALUES (%s, CURRENT_DATE, %s)'''
        cursor.execute(query, (
            alteration_data['alteration_type'],
            alteration_data['change_id']
        ))
        db.get_db().commit()
        
        return make_response(jsonify({'message': 'Alteration recorded successfully'}), 201)
    except Exception as e:
        db.get_db().rollback()
        current_app.logger.error(f'Error in create_alteration: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

# Database Management Routes
@maintenance.route('/databases', methods=['GET'])
def get_databases():
    """Get all database information"""
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT di.database_id, di.name, di.version, di.type, di.last_update,
                   ms.first_name, ms.last_name,
                   COUNT(DISTINCT ah.database_id) as alert_count,
                   COUNT(DISTINCT dah.change_id) as alteration_count
            FROM database_info di
            JOIN maintenance_staff ms ON di.staff_id = ms.staff_id
            LEFT JOIN alert_history ah ON di.database_id = ah.database_id
            LEFT JOIN data_alteration_history dah ON di.change_id = dah.change_id
            GROUP BY di.database_id, ms.staff_id
            ORDER BY di.last_update DESC
        ''')
        databases = cursor.fetchall()
        return make_response(jsonify(databases), 200)
    except Exception as e:
        current_app.logger.error(f'Error in get_databases: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)