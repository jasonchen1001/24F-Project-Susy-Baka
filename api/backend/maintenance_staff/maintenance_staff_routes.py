from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

maintenance_staff = Blueprint('maintenance_staff', __name__)

#------------------------------------------------------------
# Get all alerts
@maintenance_staff.route('/alerts', methods=['GET'])
def get_alerts():
    """Fetch all alert history"""
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT 
                ah.database_id,
                ah.metrics, 
                ah.alerts, 
                ah.severity,
                di.name AS database_name, 
                di.version AS db_version
            FROM alert_history ah
            JOIN database_info di ON ah.database_id = di.database_id
            ORDER BY ah.severity DESC
        ''')
        alerts = cursor.fetchall()
        
        if not alerts:
            return make_response(jsonify([]), 200)
            
        return make_response(jsonify(alerts), 200)
    except Exception as e:
        current_app.logger.error(f"Error in get_alerts: {str(e)}")
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Update an alert
@maintenance_staff.route('/alerts/<int:alert_id>', methods=['PUT'])
def update_alert(alert_id):
    """Update an alert"""
    try:
        cursor = db.get_db().cursor()
        alert_data = request.json

        # 检查记录是否存在
        cursor.execute('''
            SELECT database_id FROM alert_history 
            WHERE database_id = %s
        ''', (alert_id,))
        if not cursor.fetchone():
            return make_response(jsonify({'error': 'Alert not found'}), 404)

        # 更新记录
        cursor.execute('''
            UPDATE alert_history 
            SET metrics = %s, alerts = %s, severity = %s
            WHERE database_id = %s
        ''', (
            alert_data['metrics'],
            alert_data['alerts'],
            alert_data['severity'],
            alert_id
        ))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Alert updated successfully'}), 200)
    except Exception as e:
        db.get_db().rollback()
        current_app.logger.error(f"Error in update_alert: {str(e)}")
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Get all backups
@maintenance_staff.route('/backups', methods=['GET'])
def get_backups():
    """Fetch all backup history"""
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT 
                bh.database_id,
                bh.type, 
                bh.backup_date, 
                bh.details,
                di.name AS database_name, 
                di.version AS db_version
            FROM backup_history bh
            JOIN database_info di ON bh.database_id = di.database_id
            ORDER BY bh.backup_date DESC
        ''')
        backups = cursor.fetchall()
        
        if not backups:
            return make_response(jsonify([]), 200)
            
        return make_response(jsonify(backups), 200)
    except Exception as e:
        current_app.logger.error(f"Error in get_backups: {str(e)}")
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Update a backup
@maintenance_staff.route('/backups/<int:backup_id>', methods=['PUT'])
def update_backup(backup_id):
    """Update a backup record"""
    try:
        cursor = db.get_db().cursor()
        backup_data = request.json

        # 检查记录是否存在
        cursor.execute('''
            SELECT database_id FROM backup_history 
            WHERE database_id = %s
        ''', (backup_id,))
        if not cursor.fetchone():
            return make_response(jsonify({'error': 'Backup not found'}), 404)

        # 更新记录
        cursor.execute('''
            UPDATE backup_history 
            SET type = %s, backup_date = %s, details = %s
            WHERE database_id = %s
        ''', (
            backup_data['type'],
            backup_data['backup_date'],
            backup_data['details'],
            backup_id
        ))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Backup updated successfully'}), 200)
    except Exception as e:
        db.get_db().rollback()
        current_app.logger.error(f"Error in update_backup: {str(e)}")
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Get all alterations
@maintenance_staff.route('/alterations', methods=['GET'])
def get_alterations():
    """Fetch all data alteration history"""
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT 
                dah.database_id,
                dah.alteration_type, 
                dah.alteration_date,
                di.name AS database_name, 
                di.version AS db_version
            FROM data_alteration_history dah
            JOIN database_info di ON dah.database_id = di.database_id
            ORDER BY dah.alteration_date DESC
        ''')
        alterations = cursor.fetchall()
        
        if not alterations:
            return make_response(jsonify([]), 200)
            
        return make_response(jsonify(alterations), 200)
    except Exception as e:
        current_app.logger.error(f"Error in get_alterations: {str(e)}")
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Update an alteration
@maintenance_staff.route('/alterations/<int:alteration_id>', methods=['PUT'])
def update_alteration(alteration_id):
    """Update a data alteration"""
    try:
        cursor = db.get_db().cursor()
        alteration_data = request.json

        # 检查记录是否存在
        cursor.execute('''
            SELECT database_id FROM data_alteration_history 
            WHERE database_id = %s
        ''', (alteration_id,))
        if not cursor.fetchone():
            return make_response(jsonify({'error': 'Alteration not found'}), 404)

        # 更新记录
        cursor.execute('''
            UPDATE data_alteration_history 
            SET alteration_type = %s, alteration_date = %s
            WHERE database_id = %s
        ''', (
            alteration_data['alteration_type'],
            alteration_data['alteration_date'],
            alteration_id
        ))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Alteration updated successfully'}), 200)
    except Exception as e:
        db.get_db().rollback()
        current_app.logger.error(f"Error in update_alteration: {str(e)}")
        return make_response(jsonify({'error': str(e)}), 500)
    
# 在 maintenance_staff_routes.py 中添加

@maintenance_staff.route('/alterations', methods=['POST'])
def add_alteration():
    """Add a new data alteration"""
    try:
        alteration_data = request.json
        cursor = db.get_db().cursor()
        
        query = '''
            INSERT INTO data_alteration_history 
            (database_id, alteration_type, alteration_date)
            VALUES (%s, %s, %s)
        '''
        cursor.execute(query, (
            alteration_data['database_id'],
            alteration_data['alteration_type'],
            alteration_data['alteration_date']
        ))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Alteration added successfully'}), 200)
    except Exception as e:
        db.get_db().rollback()
        current_app.logger.error(f"Error in add_alteration: {str(e)}")
        return make_response(jsonify({'error': str(e)}), 500)

@maintenance_staff.route('/alterations/<int:alteration_id>', methods=['DELETE'])
def delete_alteration(alteration_id):
    """Delete a data alteration"""
    try:
        cursor = db.get_db().cursor()
        
        # 检查记录是否存在
        cursor.execute('SELECT database_id FROM data_alteration_history WHERE database_id = %s', (alteration_id,))
        if not cursor.fetchone():
            return make_response(jsonify({'error': 'Alteration not found'}), 404)
            
        # 删除记录
        cursor.execute('DELETE FROM data_alteration_history WHERE database_id = %s', (alteration_id,))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Alteration deleted successfully'}), 200)
    except Exception as e:
        db.get_db().rollback()
        current_app.logger.error(f"Error in delete_alteration: {str(e)}")
        return make_response(jsonify({'error': str(e)}), 500)
    
@maintenance_staff.route('/backups', methods=['POST'])
def add_backup():
    """Add a new backup record."""
    try:
        backup_data = request.json
        cursor = db.get_db().cursor()
        # 先检查 database_id 是否存在
        cursor.execute('SELECT database_id FROM database_info WHERE database_id = %s', 
                      (backup_data['database_id'],))
        if not cursor.fetchone():
            return make_response(jsonify({'error': 'Database not found'}), 404)
            
        query = '''
            INSERT INTO backup_history 
            (database_id, type, backup_date, details)
            VALUES (%s, %s, %s, %s)
        '''
        cursor.execute(query, (
            backup_data['database_id'],
            backup_data['type'],
            backup_data['backup_date'],
            backup_data['details']
        ))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Backup created successfully'}), 200)
    except Exception as e:
        db.get_db().rollback()
        current_app.logger.error(f"Error in add_backup: {str(e)}")
        return make_response(jsonify({'error': str(e)}), 500)

@maintenance_staff.route('/backups/<int:backup_id>', methods=['DELETE'])
def delete_backup(backup_id):
    """Delete a backup record."""
    try:
        cursor = db.get_db().cursor()
        # 检查记录是否存在
        cursor.execute('SELECT database_id FROM backup_history WHERE database_id = %s', 
                      (backup_id,))
        if not cursor.fetchone():
            return make_response(jsonify({'error': 'Backup not found'}), 404)
            
        cursor.execute('DELETE FROM backup_history WHERE database_id = %s', (backup_id,))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Backup deleted successfully'}), 200)
    except Exception as e:
        db.get_db().rollback()
        current_app.logger.error(f"Error in delete_backup: {str(e)}")
        return make_response(jsonify({'error': str(e)}), 500)

@maintenance_staff.route('/databases', methods=['GET'])
def get_databases():
    """Fetch all database information."""
    try:
        cursor = db.get_db().cursor()
        query = '''
            SELECT 
                di.database_id, di.name, di.version, di.type, di.last_update
            FROM database_info di
            ORDER BY di.last_update DESC
        '''
        cursor.execute(query)
        rows = cursor.fetchall()
        databases = []
        for row in rows:
            databases.append({
                "database_id": row[0],
                "name": row[1],
                "version": row[2],
                "type": row[3],
                "last_update": row[4]
            })
        return make_response(jsonify(databases), 200)
    except Exception as e:
        current_app.logger.error(f"Error in get_databases: {str(e)}")
        return make_response(jsonify({'error': str(e)}), 500)