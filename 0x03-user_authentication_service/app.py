#!/usr/bin/env python3
"""A basic Flask app"""

from flask import Flask, jsonify, request, abort
from auth import Auth

app = Flask(__name__)
auth = Auth()


@app.route("/", methods=['GET'], strict_slashes=False)
def index() -> str:
    """ GET /
    Return JSON payload of the form
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """
    POST /uers
    Implements the endpoint to register a user
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = auth.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": f"{email}", "message": "user created"})


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """
    POST /sessions
    Return:
        - The account login
    """
    email, password = request.form.get("email"), request.form.get("password")
    if not auth.valid_login(email, password):
        abort(401)
        session_id = auth.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def logout() -> str:
    """ DELETE / sessions
    Return:
        - Redirects to home route
    """
    session_id = request.cookies.get("session_d")
    user = authget_user_from_session_id(session_id)
    if user is None:
        abort(403)
        auth.destroy_session(user.id)
        return redirect("/")

@app.route("/profile", methods=["POST"], strict_slashes=False)
def profile() -> str:
    """
    POST /profile
    Return:
        - user email JSOn represented
    """
    session_id = request.cookies.get("session_id")
    user = auth.get_user_from_session_id(session_id)
    if not user:
        abort(403)
        return jsonify({"email": user.email})

@app.route("/reset_password", method=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    POST /reset_password
    Return:
        -
    """
    try:
        reset_token = auth.get_rest_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": f"{email}", "reser_token": f"{reset_token}"})





if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
