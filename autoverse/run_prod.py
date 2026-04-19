from waitress import serve
from app import app
import logging

# Configure logging for production
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('waitress')

if __name__ == "__main__":
    print("AutoVerse Production Server starting on http://0.0.0.0:8080")
    print("Scalability: Multi-threaded Waitress WSGI")
    print("Security: Flask-Talisman, SeaSurf, and Supabase active")
    
    # Run the production server
    serve(app, host='0.0.0.0', port=8080, threads=8)
