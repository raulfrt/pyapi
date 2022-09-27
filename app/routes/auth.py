# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify
from pyjwt import Jwt


jwt = Jwt()
route_auth = Blueprint("route_auth", __name__)


@route_auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if data.get("username") == "demo" and data.get("password") == "demo":
        return jwt.write_token(data)
    response = jsonify({"message": "User or Password not found"})
    response.status_code = 404
    return response
