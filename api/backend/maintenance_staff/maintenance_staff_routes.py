########################################################
# Maintenance Staff blueprint
########################################################
from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

maintenance = Blueprint('maintenance', __name__)

#------------------------------------------------------------
# Get system performance data (Story 5)
@maintenance.route('/system/performance', methods=['GET'])
def get_performance():
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT ah.*, di.name as database_name
            FROM alert_history ah
            JOIN database_info di ON ah.database_id = di.database_id
            ORDER BY di.last_update DESC
        ''')
        performance = cursor.fetchall()
        return make_response(jsonify(performance), 200)
    except Exception as e:
        current_app.logger.error(f'Error in get_performance: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Update monitoring parameters (Story 5)
@maintenance.route('/system/performance', methods=['PUT'])
def update_monitoring():
    try:
        monitor_data = request.json
        cursor = db.get_db().cursor()
        
        query = '''UPDATE alert_history 
                  SET metrics = %s, alerts = %s, severity = %s
                  WHERE database_id = %s'''
        data = (monitor_data['metrics'], monitor_data['alerts'],
               monitor_data['severity'], monitor_data['database_id'])
        
        cursor.execute(query, data)
        db.get_db().commit()
        
        return make_response(jsonify({'message': 'Monitoring parameters updated'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error in update_monitoring: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Get backup list (Story 6)
@maintenance.route('/system/backups', methods=['GET'])
def get_backups():
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT bh.*, di.name as database_name
            FROM backup_history bh
            JOIN database_info di ON bh.change_id = di.change_id
            ORDER BY bh.backup_date DESC
        ''')
        backups = cursor.fetchall()
        return make_response(jsonify(backups), 200)
    except Exception as e:
        current_app.logger.error(f'Error in get_backups: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Create new backup (Story 6)
@maintenance.route('/system/backups', methods=['POST'])
def create_backup():
    try:
        backup_data = request.json
        cursor = db.get_db().cursor()
        
        query = '''INSERT INTO backup_history 
                  (type, backup_date, backup_type, details, change_id)
                  VALUES (%s, CURRENT_DATE, %s, %s, %s)'''
        data = (backup_data['type'], backup_data['backup_type'],
               backup_data['details'], backup_data['change_id'])
        
        cursor.execute(query, data)
        db.get_db().commit()
        
        return make_response(jsonify({'message': 'Backup created successfully'}), 201)
    except Exception as e:
        current_app.logger.error(f'Error in create_backup: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Delete old backup (Story 5)
@maintenance.route('/system/backups/<change_id>', methods=['DELETE'])
def delete_backup(change_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('DELETE FROM backup_history WHERE change_id = %s', (change_id,))
        db.get_db().commit()
        
        if cursor.rowcount == 0:
            return make_response(jsonify({'error': 'Backup not found'}), 404)
            
        return make_response(jsonify({'message': 'Backup deleted successfully'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error in delete_backup: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Get system alerts (Story 5)
@maintenance.route('/system/alerts', methods=['GET'])
def get_alerts():
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT ah.*, di.name as database_name
            FROM alert_history ah
            JOIN database_info di ON ah.database_id = di.database_id
            ORDER BY ah.severity DESC
        ''')
        alerts = cursor.fetchall()
        return make_response(jsonify(alerts), 200)
    except Exception as e:
        current_app.logger.error(f'Error in get_alerts: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Create alert rule (Story 5)
@maintenance.route('/system/alerts', methods=['POST'])
def create_alert():
    try:
        alert_data = request.json
        cursor = db.get_db().cursor()
        
        query = '''INSERT INTO alert_history 
                  (metrics, alerts, severity, database_id)
                  VALUES (%s, %s, %s, %s)'''
        data = (alert_data['metrics'], alert_data['alerts'],
               alert_data['severity'], alert_data['database_id'])
        
        cursor.execute(query, data)
        db.get_db().commit()
        
        return make_response(jsonify({'message': 'Alert rule created successfully'}), 201)
    except Exception as e:
        current_app.logger.error(f'Error in create_alert: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Update alert status (Story 5)
@maintenance.route('/system/alerts/<database_id>', methods=['PUT'])
def update_alert(database_id):
    try:
        alert_data = request.json
        cursor = db.get_db().cursor()
        
        query = '''UPDATE alert_history 
                  SET metrics = %s, alerts = %s, severity = %s
                  WHERE database_id = %s'''
        data = (alert_data['metrics'], alert_data['alerts'],
               alert_data['severity'], database_id)
        
        cursor.execute(query, data)
        db.get_db().commit()
        
        if cursor.rowcount == 0:
            return make_response(jsonify({'error': 'Alert not found'}), 404)
            
        return make_response(jsonify({'message': 'Alert updated successfully'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error in update_alert: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Delete alert (Story 5)
@maintenance.route('/system/alerts/<database_id>', methods=['DELETE'])
def delete_alert(database_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('DELETE FROM alert_history WHERE database_id = %s', (database_id,))
        db.get_db().commit()
        
        if cursor.rowcount == 0:
            return make_response(jsonify({'error': 'Alert not found'}), 404)
            
        return make_response(jsonify({'message': 'Alert deleted successfully'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error in delete_alert: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Get maintenance tasks (Story 4)
@maintenance.route('/system/maintenance', methods=['GET'])
def get_maintenance_tasks():
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT dah.*, di.name as database_name
            FROM data_alteration_history dah
            JOIN database_info di ON dah.change_id = di.change_id
            ORDER BY dah.alteration_date DESC
        ''')
        tasks = cursor.fetchall()
        return make_response(jsonify(tasks), 200)
    except Exception as e:
        current_app.logger.error(f'Error in get_maintenance_tasks: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Create maintenance task (Story 4)
@maintenance.route('/system/maintenance', methods=['POST'])
def create_task():
    try:
        task_data = request.json
        cursor = db.get_db().cursor()
        
        query = '''INSERT INTO data_alteration_history 
                  (alteration_type, alteration_date, change_id)
                  VALUES (%s, CURRENT_DATE, %s)'''
        data = (task_data['alteration_type'], task_data['change_id'])
        
        cursor.execute(query, data)
        db.get_db().commit()
        
        return make_response(jsonify({'message': 'Maintenance task created successfully'}), 201)
    except Exception as e:
        current_app.logger.error(f'Error in create_task: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Update task status (Story 4)
@maintenance.route('/system/maintenance/<change_id>', methods=['PUT'])
def update_task(change_id):
    try:
        task_data = request.json
        cursor = db.get_db().cursor()
        
        query = '''UPDATE data_alteration_history 
                  SET alteration_type = %s
                  WHERE change_id = %s'''
        data = (task_data['alteration_type'], change_id)
        
        cursor.execute(query, data)
        db.get_db().commit()
        
        if cursor.rowcount == 0:
            return make_response(jsonify({'error': 'Task not found'}), 404)
            
        return make_response(jsonify({'message': 'Task updated successfully'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error in update_task: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Delete task (Story 4)
@maintenance.route('/system/maintenance/<change_id>', methods=['DELETE'])
def delete_task(change_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('DELETE FROM data_alteration_history WHERE change_id = %s', (change_id,))
        db.get_db().commit()
        
        if cursor.rowcount == 0:
            return make_response(jsonify({'error': 'Task not found'}), 404)
            
        return make_response(jsonify({'message': 'Task deleted successfully'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error in delete_task: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Get schema info (Story 1)
@maintenance.route('/system/schema', methods=['GET'])
def get_schema():
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT di.*
            FROM database_info di
            ORDER BY di.last_update DESC
        ''')
        schema = cursor.fetchall()
        return make_response(jsonify(schema), 200)
    except Exception as e:
        current_app.logger.error(f'Error in get_schema: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Update schema (Story 1)
@maintenance.route('/system/schema/<database_id>', methods=['PUT'])
def update_schema(database_id):
    try:
        schema_data = request.json
        cursor = db.get_db().cursor()
        
        query = '''UPDATE database_info 
                  SET name = %s, version = %s, type = %s, last_update = CURRENT_DATE
                  WHERE database_id = %s'''
        data = (schema_data['name'], schema_data['version'], 
               schema_data['type'], database_id)
        
        cursor.execute(query, data)
        db.get_db().commit()
        
        if cursor.rowcount == 0:
            return make_response(jsonify({'error': 'Schema not found'}), 404)
            
        return make_response(jsonify({'message': 'Schema updated successfully'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error in update_schema: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

#------------------------------------------------------------
# Remove obsolete schema (Story 3)
@maintenance.route('/system/schema/<database_id>', methods=['DELETE'])
def remove_schema(database_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('DELETE FROM database_info WHERE database_id = %s', (database_id,))
        db.get_db().commit()
        
        if cursor.rowcount == 0:
            return make_response(jsonify({'error': 'Schema not found'}), 404)
            
        return make_response(jsonify({'message': 'Schema removed successfully'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error in remove_schema: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)