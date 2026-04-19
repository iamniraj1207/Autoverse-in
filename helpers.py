"""
helpers.py — Utility functions for AutoVerse
- login_required decorator
- Error response helpers
"""
from functools import wraps
from flask import redirect, session, url_for, jsonify


def login_required(f):
    """
    Decorator: redirect unauthenticated users to /login.
    Usage: @login_required on any route function.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


def error_response(message, code=400):
    """Return a standardised JSON error for API routes."""
    return jsonify({"error": message}), code


def success_response(data=None, message="ok"):
    """Return a standardised JSON success payload for API routes."""
    payload = {"status": message}
    if data is not None:
        payload["data"] = data
    return jsonify(payload), 200
