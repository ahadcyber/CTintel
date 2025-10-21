"""
WSGI entry point for production deployment
Use with Gunicorn, uWSGI, or Waitress
"""
import os
import sys

# Add project directory to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Import application
from web.app_enhanced import app as application

if __name__ == "__main__":
    # For testing WSGI locally
    application.run()
