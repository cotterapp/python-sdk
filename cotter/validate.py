import requests
import os
from jose import jwt

CotterJWKSURL = "https://www.cotter.app/api/v0/token/jwks"


def validate_access_token(access_token, api_key):
    # Getting jwt key
    r = requests.get(url=CotterJWKSURL)
    data = r.json()
    public_key = data["keys"][0]

    # Getting access token and validate it
    # This library also makes sure token is not expired
    # and that the audience is correct
    access_token_resp = jwt.decode(
        access_token, public_key, algorithms='ES256', audience=api_key)

    return access_token_resp


def validate_id_token(id_token, api_key):
    # Getting jwt key
    r = requests.get(url=CotterJWKSURL)
    data = r.json()
    public_key = data["keys"][0]

    # Getting id token and validate it
    # This library also makes sure token is not expired
    # and that the audience is correct
    id_token_resp = jwt.decode(
        id_token, public_key, algorithms='ES256', audience=api_key)

    return id_token_resp
