"""
Google Cloud Storage utilities
Handles signed URL generation for secure uploads
"""

import os
from datetime import timedelta
from google.cloud import storage
from config import GCS_BUCKET_NAME, GCS_SERVICE_ACCOUNT_PATH, GCS_SIGNED_URL_EXPIRATION
from .logger import logger


def generate_signed_upload_url(officer_id, file_extension='jpg'):
    """
    Generate a signed URL for uploading a selfie image to Google Cloud Storage.
    
    Args:
        officer_id (str): Officer ID to include in the filename
        file_extension (str): File extension (default: 'jpg')
        
    Returns:
        dict: {
            'signed_url': str,
            'file_path': str,
            'expires_in': int
        }
        
    Raises:
        Exception: If signed URL generation fails
    """
    try:
        # Initialize GCS client with service account
        client = storage.Client.from_service_account_json(GCS_SERVICE_ACCOUNT_PATH)
        bucket = client.bucket(GCS_BUCKET_NAME)
        
        # Generate unique filename: selfies/officer_GP12345_timestamp.jpg
        from datetime import datetime
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        file_path = f"selfies/{officer_id}_{timestamp}.{file_extension}"
        
        # Create blob reference
        blob = bucket.blob(file_path)
        
        # Generate signed URL for PUT operation (upload)
        signed_url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(seconds=GCS_SIGNED_URL_EXPIRATION),
            method="PUT",
            content_type=f"image/{file_extension}"
        )
        
        logger.info(f"Generated signed URL for officer {officer_id}: {file_path}")
        
        return {
            'signed_url': signed_url,
            'file_path': file_path,
            'expires_in': GCS_SIGNED_URL_EXPIRATION
        }
    
    except Exception as e:
        logger.error(f"Failed to generate signed URL: {str(e)}")
        raise Exception(f"Signed URL generation failed: {str(e)}")
