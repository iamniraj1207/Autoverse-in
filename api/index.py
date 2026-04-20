import sys
import os

# Add the parent directory to sys.path so we can import from the root
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import the Flask app instance from the root app.py
from app import app
