"""
Admin Routes
Defines admin API endpoints
"""

from flask import Blueprint, request
from controllers.admin_controller import AdminController
from utils.security import require_admin_key
from utils.responses import ResponseHelper
from utils.logger import log_request, get_client_ip

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/execute-sql', methods=['POST'])
def execute_sql():
    """
    Admin-only SQL execution endpoint.
    Requires x-admin-key header.
    
    Request:
        POST /admin/execute-sql
        Headers:
            x-admin-key: <admin_key>
            Content-Type: application/json
        Body:
            {
                "query": "SQL QUERY HERE"
            }
    
    Response:
        SELECT queries:
            {
                "success": true,
                "type": "select",
                "rows": [...]
            }
        
        INSERT/UPDATE/DELETE queries:
            {
                "success": true,
                "type": "write",
                "rows_affected": <number>
            }
    """
    client_ip = get_client_ip()
    
    # Check admin authorization
    auth_error = require_admin_key()
    if auth_error:
        return auth_error
    
    # Validate Content-Type
    if not request.is_json:
        log_request(client_ip, '/admin/execute-sql', 'error', 'Invalid Content-Type')
        return ResponseHelper.error('Content-Type must be application/json')
    
    # Validate input
    data = request.get_json()
    if not data or 'query' not in data:
        log_request(client_ip, '/admin/execute-sql', 'error', 'Missing query parameter')
        return ResponseHelper.error('Missing query parameter')
    
    query = data.get('query')
    
    if not isinstance(query, str):
        log_request(client_ip, '/admin/execute-sql', 'error', 'Query must be a string')
        return ResponseHelper.error('Query must be a string')
    
    if not query.strip():
        log_request(client_ip, '/admin/execute-sql', 'error', 'Query cannot be empty')
        return ResponseHelper.error('Query cannot be empty')
    
    # Execute query via controller
    return AdminController.execute_sql(query)
