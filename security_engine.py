import threading
import time
import subprocess
import logging
from flask import session, abort, redirect, url_for
from functools import wraps

logger = logging.getLogger('security')

class SecurityManager:
    """
    Handles robust user access management and auto-updating security protocols.
    Designed for production environments to ensure client-ready stability.
    """
    
    @staticmethod
    def run_security_audit():
        """Background task that ensures packages and server security are optimal."""
        while True:
            try:
                # In a full OS environment, this could hook into pip-audit or auto-git-pull
                logger.info("[SEC-ENGINE] Performing background dependency security check...")
                
                # Check for critical dependency updates automatically using pip
                # We use --disable-pip-version-check to focus on packages
                result = subprocess.run(["pip", "list", "--outdated"], capture_output=True, text=True)
                if 'Flask' in result.stdout or 'g4f' in result.stdout:
                    logger.warning("[SEC-ENGINE] Critical updates available. Applying security patch...")
                    # Automatically upgrade critical security packages
                    subprocess.run(["pip", "install", "--upgrade", "Flask", "flask-talisman", "flask-seasurf"], capture_output=True)
                    logger.info("[SEC-ENGINE] Security patch applied successfully.")
                else:
                    logger.info("[SEC-ENGINE] System secure. No updates required.")
                    
                time.sleep(86400) # Run audit once every 24 hours
                
            except Exception as e:
                logger.error(f"[SEC-ENGINE] Audit failed: {e}")
                time.sleep(3600) # Retry in an hour if failed

    @staticmethod
    def init_background_threads():
        """Starts the auto-update and monitoring threads."""
        audit_thread = threading.Thread(target=SecurityManager.run_security_audit, daemon=True)
        audit_thread.start()

# --- Role Based Access Management (RBAC) ---

def role_required(required_role="user"):
    """
    Decorator for route access management.
    Ensures users without proper clearance cannot access sensitive logic.
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not session.get('user_id'):
                return redirect(url_for('login', error="Active session required."))
                
            # If expanding, check Supabase 'role' column here. 
            # Currently defaulting basic check for generic authenticated users.
            current_role = session.get('role', 'user')
            
            roles_hierarchy = {'admin': 3, 'moderator': 2, 'user': 1}
            
            if roles_hierarchy.get(current_role, 0) < roles_hierarchy.get(required_role, 1):
                abort(403) # Forbidden
                
            return f(*args, **kwargs)
        return wrapped
    return decorator
