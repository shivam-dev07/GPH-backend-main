"""
Police Patrolling App - Flask Backend Server
Main application entry point with Flask factory pattern
"""

from flask import Flask, request
from flask_cors import CORS
from config import ALLOWED_ORIGINS, FORCE_HTTPS, DB_CONFIG, ALLOW_WRITE_QUERIES, SERVER_HOST, SERVER_PORT, DEBUG_MODE
from routes import admin_bp, public_bp, upload_bp
from routes.duty_routes import duty_bp
from routes.vehicle_routes import vehicle_bp
from routes.activity_routes import activity_bp
from routes.live_location_routes import live_location_bp
from routes.compliance_routes import compliance_bp
from routes.notification_routes import notification_bp
from routes.check_in_routes import check_in_bp
from routes.duty_location_routes import duty_location_bp
from routes.officer_routes import officer_bp
from routes.auth_routes import auth_bp
from utils.responses import ResponseHelper
from utils.logger import logger


def create_app():
    """
    Application factory pattern.
    Creates and configures the Flask application.
    
    Returns:
        Flask: Configured Flask application
    """
    app = Flask(__name__)
    
    # CORS configuration
    if ALLOWED_ORIGINS == '*':
        CORS(app, resources={r"/*": {"origins": "*"}})
    else:
        origins = [origin.strip() for origin in ALLOWED_ORIGINS.split(',')]
        CORS(app, resources={r"/*": {"origins": origins}})
    
    # Register blueprints (controllers)
    app.register_blueprint(admin_bp)
    app.register_blueprint(public_bp)
    app.register_blueprint(upload_bp)

    # Register new API blueprints
    app.register_blueprint(duty_bp)
    app.register_blueprint(vehicle_bp)
    app.register_blueprint(activity_bp)
    app.register_blueprint(live_location_bp)
    app.register_blueprint(compliance_bp)
    app.register_blueprint(notification_bp)
    app.register_blueprint(check_in_bp)
    app.register_blueprint(duty_location_bp)
    app.register_blueprint(officer_bp)
    app.register_blueprint(auth_bp)
    
    # Global error handlers
    @app.errorhandler(404)
    def not_found(e):
        return ResponseHelper.error('Endpoint not found', 404)
    
    @app.errorhandler(405)
    def method_not_allowed(e):
        return ResponseHelper.error('Method not allowed', 405)
    
    @app.errorhandler(500)
    def internal_error(e):
        logger.error(f"Internal server error: {str(e)}")
        return ResponseHelper.internal_error()
    
    # HTTPS enforcement (if enabled)
    @app.before_request
    def enforce_https():
        if FORCE_HTTPS and not request.is_secure and request.headers.get('X-Forwarded-Proto') != 'https':
            return ResponseHelper.error('HTTPS required', 403)
    
    return app


if __name__ == '__main__':
    app = create_app()
    
    logger.info("="*60)
    logger.info("Police Patrolling App - Flask Backend Server Starting")
    logger.info("="*60)
    logger.info(f"Database: {DB_CONFIG['database']} @ {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    logger.info(f"CORS Origins: {ALLOWED_ORIGINS}")
    logger.info(f"HTTPS Enforcement: {FORCE_HTTPS}")
    logger.info(f"Write Queries Allowed: {ALLOW_WRITE_QUERIES}")
    logger.info("="*60)
    
    # Run development server
    app.run(
        host=SERVER_HOST,
        port=SERVER_PORT,
        debug=DEBUG_MODE
    )
