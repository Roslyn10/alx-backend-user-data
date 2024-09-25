#!/usr/bin/env python3
"""A basic Flask app"""

from flask import Flask, jsonify
from auth import Auth

app = Flask(__name__)
auth = Auth()


@app.route("/", methods=['GET'], strict_slashes=False)
def index() -> str:
    """ GET /
    Return JSON payload of the form
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/", methods=['POST'], strict_slashes=False)
def users(self, email: str, password: str) -> str:
    """POST /
    Implements the end-point to register a user
    """
    email, password = request.form.get("email"), request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({
            "email": "<registered email>", "message": "user created"
            })
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
