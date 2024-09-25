#!/usr/bin/env python3
"""A basic Flask app"""

from flask import Flask, jsonify, abort, request, redirect
from auth import Auth

app = Flask(__name__)
auth = Auth()


@app.route("/", method=['GET'], strict_slashes=Flase)
def index(): -> str:
    """ GET /
    Return JSON payload of the form
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
