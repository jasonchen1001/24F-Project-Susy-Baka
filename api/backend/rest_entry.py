from flask import Flask
from backend.db_connection import db
from backend.hr.hr_routes import hr_bp  # 只保留我们需要的 hr 模块
import os
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)

    # Load environment variables
    load_dotenv()

    # Configure app
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['MYSQL_DATABASE_USER'] = os.getenv('DB_USER').strip()
    app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_ROOT_PASSWORD').strip()
    app.config['MYSQL_DATABASE_HOST'] = os.getenv('DB_HOST').strip()
    app.config['MYSQL_DATABASE_PORT'] = int(os.getenv('DB_PORT').strip())
    app.config['MYSQL_DATABASE_DB'] = os.getenv('DB_NAME').strip()

    # Initialize database
    app.logger.info('current_app(): starting the database connection')
    db.init_app(app)

    # Register blueprints
    app.logger.info('current_app(): registering blueprints with Flask app object.')   
    app.register_blueprint(hr_bp, url_prefix='/hr')  # 只注册 hr blueprint

    return app

