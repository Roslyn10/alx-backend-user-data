#!/usr/bin/env python3
""" Flask view that handles all routes for the Session Authentication"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    POST /auth_session/login: Creates a session for a user
    """
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth

            session_id = auth.create_session(user.id)

            SESSION_NAME = getenv("SESSION_NAME")

            response = jsonify(user.to_json())
            response.set_cookie(SESSION_NAME, session_id)

            return response
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """
    DELETE /auth_session/logout:
    Deletes a session for a user
    """
    from api.v1.app import auth
    is_deleted = auth.destroy_session(request)

    if not is_deleted:
        abort(404)

    return jsonify({}), 200
