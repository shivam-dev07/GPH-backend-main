"""
Upload Routes
Defines upload API endpoints
"""

from flask import Blueprint, request
from controllers.upload_controller import UploadController
from utils.responses import ResponseHelper
from utils.logger import log_request, get_client_ip

upload_bp = Blueprint('upload', __name__, url_prefix='/upload')


@upload_bp.route('/request-url', methods=['POST'])
def request_upload_url():
    """
    Request a signed URL for uploading selfie image.
    
    Request:
        POST /upload/request-url
        Headers:
            Content-Type: application/json
        Body:
            {
                "officer_id": "GP02650"
            }
    
    Response:
        {
            "success": true,
            "data": {
                "signed_url": "https://storage.googleapis.com/...",
                "file_path": "selfies/GP02650_20251115_123456.jpg",
                "expires_in_seconds": 900,
                "upload_method": "PUT",
                "content_type": "image/jpeg"
            }
        }
    """
    client_ip = get_client_ip()
    
    # Validate Content-Type
    if not request.is_json:
        log_request(client_ip, '/upload/request-url', 'error', 'Invalid Content-Type')
        return ResponseHelper.error('Content-Type must be application/json')
    
    # Validate input
    data = request.get_json()
    if not data or 'officer_id' not in data:
        log_request(client_ip, '/upload/request-url', 'error', 'Missing officer_id')
        return ResponseHelper.error('Missing officer_id parameter')
    
    officer_id = data.get('officer_id')
    
    if not isinstance(officer_id, str):
        log_request(client_ip, '/upload/request-url', 'error', 'officer_id must be a string')
        return ResponseHelper.error('officer_id must be a string')
    
    # Call controller
    return UploadController.request_upload_url(officer_id)
