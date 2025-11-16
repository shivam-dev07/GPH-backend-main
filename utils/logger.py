"""
Logging utilities
Handles request logging and application logging
"""

import sys
import logging
from datetime import datetime
from flask import request

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%S',
    handlers=[
        logging.FileHandler('sql_queries.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def log_request(client_ip, query_or_path, status, error_msg=None):
    """
    Log all requests with timestamp, IP, query/path, status, and error.
    
    Args:
        client_ip (str): Client IP address
        query_or_path (str): SQL query or API path
        status (str): Request status (success/error/blocked/unauthorized)
        error_msg (str, optional): Error message if any
    """
    timestamp = datetime.utcnow().isoformat() + 'Z'
    
    # Truncate long queries
    if len(query_or_path) > 500:
        query_or_path = query_or_path[:500] + '... [TRUNCATED]'
    
    log_entry = {
        'timestamp': timestamp,
        'client_ip': client_ip,
        'query_or_path': query_or_path,
        'status': status
    }
    
    if error_msg:
        log_entry['error'] = error_msg
    
    logger.info(f"REQUEST_LOG: {log_entry}")


def get_client_ip():
    """
    Get client IP from request, respecting X-Forwarded-For header.
    
    Returns:
        str: Client IP address
    """
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    return request.remote_addr or 'unknown'


def log_info(message):
    """
    Log informational message.
    
    Args:
        message (str): Message to log
    """
    logger.info(message)


def log_error(message):
    """
    Log error message.
    
    Args:
        message (str): Error message to log
    """
    logger.error(message)
