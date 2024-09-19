#!/usr/bin/env python3
""" Flask view that handles all routes for the Session Authentication"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv

@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    """
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password mising"})

    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    for user in found_users:
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401

        from api.v1.app import auth
        
        user = found_users[0]
        session_id = auth.create_session(user.id)

        SESSION_NAME = getenv("SESSION_NAME")
        
        response = jsonify(user.to_json())
        response.set_cookie(SESSION_NAME, session_id)

        return response
