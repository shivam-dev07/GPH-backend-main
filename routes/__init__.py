"""
Routes package
Contains Flask blueprints for routing
"""

from .admin_routes import admin_bp
from .public_routes import public_bp
from .upload_routes import upload_bp

__all__ = ['admin_bp', 'public_bp', 'upload_bp']
