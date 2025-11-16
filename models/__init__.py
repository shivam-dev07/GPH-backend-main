"""
Models package
Contains database connection and data access layers
"""

from .db import get_connection
from .admin_model import AdminModel
from .officer_model import OfficerModel

__all__ = ['get_connection', 'AdminModel', 'OfficerModel']
