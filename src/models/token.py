from flask import request

def create_token():
    """Create a access token from the JWT."""
    return {
        "user_id": request.headers.get('X-User-Id'),
        "roles": request.headers.get('X-User-Roles')
    }