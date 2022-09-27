# -*- coding: utf-8 -*-

from jwt import encode, decode, exceptions
from datetime import datetime, timedelta
from flask import jsonify


class Jwt:
    def __init__(self, secret_key="mysecretkeydummy", algorithm="HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def get_expiration_date(self, minutes):
        return datetime.now() + timedelta(minutes)

    def write_token(self, data):
        payload = {
            **data,
            "exp": self.get_expiration_date(60)
        }
        token = encode(payload, self.secret_key, self.algorithm)
        return token.encode("UTF-8")

    def validate_token(self, token):
        try:
            decode(token, self.secret_key, self.algorithm)
        except exceptions.DecodeError:
            response = jsonify({
                "message": "Invalid Token"
            })
            response.status_code = 401
            return response
        except exceptions.ExpiredSignatureError:
            response = jsonify({
                "message": "Expired Token"
            })
            response.status_code = 401
            return response
