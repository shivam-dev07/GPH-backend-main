"""
EXAMPLE: Duty Routes with JWT Protection
This is an EXAMPLE file showing how to add JWT authentication to your routes.

INSTRUCTIONS:
1. Review this example
2. Update your actual routes/duty_routes.py file with @jwt_required decorators
3. Test with valid JWT tokens
"""

from flask import Blueprint, request
from controllers.duty_controller import DutyController
from utils.decorators import jwt_required  # Import the JWT decorator
from utils.responses import error_response

duty_bp = Blueprint('duty', __name__, url_prefix='/api/duties')


# PUBLIC ROUTE - No authentication required (maybe for admin dashboard)
@duty_bp.route('', methods=['GET'])
def get_all_duties():
    """GET /api/duties - Get all duties (public/admin)"""
    return DutyController.get_all_duties()


# PROTECTED ROUTE - Requires JWT authentication
@duty_bp.route('/active', methods=['GET'])
@jwt_required  # ← Add this decorator
def get_active_duties():
    """
    GET /api/duties/active - Get active duties for authenticated officer
    
    Headers:
        Authorization: Bearer <jwt_token>
    """
    # Access authenticated officer data
    officer_id = request.current_user['officer_id']
    rank = request.current_user['rank']
    
    # You can now filter duties based on the authenticated officer
    return DutyController.get_active_duties_for_officer(officer_id)


# PROTECTED ROUTE - Officer can only access their own duties
@duty_bp.route('/officer/<officer_id>', methods=['GET'])
@jwt_required  # ← Add this decorator
def get_duties_by_officer(officer_id):
    """
    GET /api/duties/officer/:officer_id - Get duties for specific officer
    
    Security: Officer can only view their own duties unless they're admin
    """
    authenticated_officer_id = request.current_user['officer_id']
    
    # Security check: Officers can only view their own duties
    if officer_id != authenticated_officer_id:
        # You might want to check if the user is admin here
        # For now, we'll deny access
        return error_response("You can only view your own duties", 403)
    
    return DutyController.get_duties_by_officer(officer_id)


# PROTECTED ROUTE - Any authenticated officer can view duty details
@duty_bp.route('/<duty_id>', methods=['GET'])
@jwt_required  # ← Add this decorator
def get_duty(duty_id):
    """GET /api/duties/:id - Get duty by ID"""
    officer_id = request.current_user['officer_id']
    
    # Optionally, verify the officer is assigned to this duty
    return DutyController.get_duty(duty_id, officer_id)


# ADMIN ONLY ROUTE - Create new duty
@duty_bp.route('', methods=['POST'])
@jwt_required  # ← Add this decorator
def create_duty():
    """
    POST /api/duties - Create new duty (ADMIN ONLY)
    
    Security: Only admins should be able to create duties
    """
    officer_id = request.current_user['officer_id']
    
    # TODO: Implement admin check
    # if not is_admin(officer_id):
    #     return error_response("Admin access required", 403)
    
    duty_data = request.get_json()
    return DutyController.create_duty(duty_data, created_by=officer_id)


# ADMIN ONLY ROUTE - Update duty
@duty_bp.route('/<duty_id>', methods=['PUT', 'PATCH'])
@jwt_required  # ← Add this decorator
def update_duty(duty_id):
    """
    PUT/PATCH /api/duties/:id - Update duty (ADMIN ONLY)
    """
    officer_id = request.current_user['officer_id']
    
    # TODO: Implement admin check
    
    updates = request.get_json()
    return DutyController.update_duty(duty_id, updates, updated_by=officer_id)


# ADMIN ONLY ROUTE - Delete duty
@duty_bp.route('/<duty_id>', methods=['DELETE'])
@jwt_required  # ← Add this decorator
def delete_duty(duty_id):
    """
    DELETE /api/duties/:id - Delete duty (ADMIN ONLY)
    """
    officer_id = request.current_user['officer_id']
    
    # TODO: Implement admin check
    
    return DutyController.delete_duty(duty_id, deleted_by=officer_id)


# NEW PROTECTED ROUTE - My Duties (convenience endpoint)
@duty_bp.route('/my-duties', methods=['GET'])
@jwt_required  # ← Add this decorator
def get_my_duties():
    """
    GET /api/duties/my-duties - Get duties for the authenticated officer
    
    This is a convenience endpoint that automatically uses the authenticated officer's ID
    """
    officer_id = request.current_user['officer_id']
    staff_name = request.current_user.get('staff_name', 'Officer')
    
    return DutyController.get_duties_by_officer(officer_id)


# NEW PROTECTED ROUTE - Check-in to duty
@duty_bp.route('/<duty_id>/check-in', methods=['POST'])
@jwt_required  # ← Add this decorator
def check_in_to_duty(duty_id):
    """
    POST /api/duties/:duty_id/check-in - Check in to a duty
    
    Request body:
        {
            "location": {"lat": 15.4909, "lng": 73.8278},
            "selfie_url": "https://storage.googleapis.com/..."
        }
    """
    officer_id = request.current_user['officer_id']
    check_in_data = request.get_json()
    
    return DutyController.check_in(duty_id, officer_id, check_in_data)


# NEW PROTECTED ROUTE - Check-out from duty
@duty_bp.route('/<duty_id>/check-out', methods=['POST'])
@jwt_required  # ← Add this decorator
def check_out_from_duty(duty_id):
    """
    POST /api/duties/:duty_id/check-out - Check out from a duty
    """
    officer_id = request.current_user['officer_id']
    check_out_data = request.get_json()
    
    return DutyController.check_out(duty_id, officer_id, check_out_data)
