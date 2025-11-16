"""
Admin Controller
Handles admin operations business logic
"""

from models.admin_model import AdminModel
from utils.responses import ResponseHelper
from utils.logger import logger, log_request, get_client_ip


class AdminController:
    """Controller for admin operations"""
    
    @staticmethod
    def execute_sql(query):
        """
        Execute SQL query with full validation and logging.
        
        Args:
            query (str): SQL query string
            
        Returns:
            tuple: (response, status_code)
        """
        client_ip = get_client_ip()
        
        try:
            # Execute query through model layer
            result = AdminModel.execute_raw_query(query)
            
            # Log successful execution
            log_request(client_ip, query, 'success')
            
            # Return appropriate response
            if result['type'] == 'select':
                return ResponseHelper.success_select(result['rows'])
            else:
                return ResponseHelper.success_write(result['rows_affected'])
        
        except ValueError as e:
            # Handle validation errors (query too long, dangerous query)
            error_msg = str(e)
            log_request(client_ip, query, 'blocked', error_msg)
            return ResponseHelper.blocked(error_msg)
        
        except Exception as e:
            # Handle database errors
            error_msg = str(e)
            logger.error(f"SQL execution error: {error_msg}")
            log_request(client_ip, query, 'error', error_msg)
            return ResponseHelper.internal_error()
