"""
Public Controller
Handles public API operations business logic
"""

from datetime import datetime
from models.officer_model import OfficerModel
from models.db import check_health
from utils.responses import ResponseHelper
from utils.logger import logger, log_request, get_client_ip


class PublicController:
    """Controller for public API operations"""
    
    @staticmethod
    def health_check():
        """
        Check system and database health.
        
        Returns:
            tuple: (response, status_code)
        """
        client_ip = get_client_ip()
        
        try:
            db_healthy = check_health()
            
            if db_healthy:
                log_request(client_ip, '/health', 'success')
                return ResponseHelper.success_data({
                    'status': 'healthy',
                    'database': 'connected',
                    'timestamp': datetime.utcnow().isoformat() + 'Z'
                })
            else:
                log_request(client_ip, '/health', 'error', 'Database connection failed')
                return ResponseHelper.error('Database connection failed', 503)
        
        except Exception as e:
            logger.error(f"Health check error: {str(e)}")
            log_request(client_ip, '/health', 'error', str(e))
            return ResponseHelper.internal_error()
    
    @staticmethod
    def get_all_officers():
        """
        Get all officers.
        
        Returns:
            tuple: (response, status_code)
        """
        client_ip = get_client_ip()
        
        try:
            # Controller calls model function (thin controller)
            officers = OfficerModel.get_all_officers()
            
            log_request(client_ip, '/officers', 'success')
            return ResponseHelper.success_data(officers)
        
        except Exception as e:
            logger.error(f"Error fetching officers: {str(e)}")
            log_request(client_ip, '/officers', 'error', str(e))
            return ResponseHelper.internal_error()
    
    @staticmethod
    def get_officer_by_id(officer_id):
        """
        Get officer by ID.
        
        Args:
            officer_id (str): Officer ID
            
        Returns:
            tuple: (response, status_code)
        """
        client_ip = get_client_ip()
        path = f'/officers/{officer_id}'
        
        try:
            # Validate officer_id
            if not officer_id or not officer_id.strip():
                log_request(client_ip, path, 'error', 'Invalid officer ID')
                return ResponseHelper.error('Invalid officer ID')
            
            # Controller calls model function (thin controller)
            officer = OfficerModel.get_officer_by_id(officer_id)
            
            if not officer:
                log_request(client_ip, path, 'error', 'Officer not found')
                return ResponseHelper.error('Officer not found', 404)
            
            log_request(client_ip, path, 'success')
            return ResponseHelper.success_data(officer)
        
        except Exception as e:
            logger.error(f"Error fetching officer {officer_id}: {str(e)}")
            log_request(client_ip, path, 'error', str(e))
            return ResponseHelper.internal_error()
