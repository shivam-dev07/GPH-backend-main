"""
Upload Controller
Handles upload operations business logic
"""

from utils.storage import generate_signed_upload_url
from utils.responses import ResponseHelper
from utils.logger import logger, log_request, get_client_ip


class UploadController:
    """Controller for upload operations"""
    
    @staticmethod
    def request_upload_url(officer_id):
        """
        Generate and return a signed URL for officer selfie upload.
        
        Args:
            officer_id (str): Officer ID requesting upload
            
        Returns:
            tuple: (response, status_code)
        """
        client_ip = get_client_ip()
        path = f'/upload/request-url'
        
        try:
            # Validate officer_id
            if not officer_id or not officer_id.strip():
                log_request(client_ip, path, 'error', 'Missing officer_id')
                return ResponseHelper.error('officer_id is required')
            
            # Generate signed URL
            result = generate_signed_upload_url(officer_id)
            
            log_request(client_ip, path, 'success', f'Signed URL generated for {officer_id}')
            
            return ResponseHelper.success_data({
                'signed_url': result['signed_url'],
                'file_path': result['file_path'],
                'expires_in_seconds': result['expires_in'],
                'upload_method': 'PUT',
                'content_type': 'image/jpeg'
            })
        
        except Exception as e:
            logger.error(f"Error generating upload URL for {officer_id}: {str(e)}")
            log_request(client_ip, path, 'error', str(e))
            return ResponseHelper.internal_error()
