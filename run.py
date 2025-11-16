"""
Start script for Police Patrolling App Backend
Run this script to start the Flask server
"""

import sys
import os

# Add backend directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

# Import and run the app
from app import create_app
from utils.logger import logger
from config import DB_CONFIG, ALLOWED_ORIGINS, FORCE_HTTPS, ALLOW_WRITE_QUERIES, SERVER_HOST, SERVER_PORT, DEBUG_MODE

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
