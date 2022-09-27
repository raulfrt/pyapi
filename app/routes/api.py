
# -*- coding: utf-8 -*-

from time import sleep
from flask import Blueprint, request
from pyjwt import Jwt
from scraping import ScrapingDisco

jwt = Jwt()
route_api = Blueprint("route_api", __name__)

# wait for the selenium server to be running
sleep(5)
sd = ScrapingDisco()


@route_api.before_request
def verify_toke():
    token = request.headers["Authorization"].split(" ")[1]
    jwt.validate_token(token)


@route_api.route("/scraping-disco", methods=["GET"])
def scraping():
    first_page = int(request.headers.get("first_page", 0))
    sd.first_page = first_page
    response = sd.scraping()
    return response
