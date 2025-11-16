"""
WSGI entry point for production deployment
Used by Gunicorn to run the Flask application
"""

from app import create_app

# Create the Flask application
application = create_app()
app = application

if __name__ == "__main__":
    app.run()
