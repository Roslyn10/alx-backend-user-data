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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
