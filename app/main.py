# -*- coding: utf-8 -*-

from flask import Flask
from routes.auth import route_auth as auth
from routes.api import route_api as api

app = Flask(__name__)
app.register_blueprint(auth, url_prefix="/api")
app.register_blueprint(api, url_prefix="/api")

# init Flask server
if __name__ == '__main__':
    app.run(port=5000, host="0.0.0.0")
