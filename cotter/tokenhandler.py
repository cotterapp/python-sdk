import json
import requests
from cotter import validate
from cotter import errors


def store_token_to_file(oauth_token, filename):
    json_token = json.dumps(oauth_token)
    f = open(filename, "w")
    f.write(json_token)
    f.close()


def get_token_from_file(filename, api_key):
    with open(filename) as json_file:
        data = json.load(json_file)

    # Refresh if needed
    oauth_token = refresh_token(data, api_key)
    store_token_to_file(oauth_token, filename)
    return oauth_token


def refresh_token(oauth_token, api_key):
    # Check if token expired
    try:
        access_token_resp = validate.validate_access_token(
            oauth_token["access_token"])
        return oauth_token
    except:
        # if token invalid, try refreshing it
        if len(oauth_token["refresh_token"]) <= 0:
            raise errors.RefreshTokenNotExistError
        # Refresh tokens using refresh_token
        url = 'https://www.cotter.app/api/v0/token/' + api_key
        headers = {'Content-Type': 'application/json', 'API_KEY_ID': api_key}
        data = {
            "grant_type": "refresh_token",
            "refresh_token": oauth_token["refresh_token"]
        }
        response = requests.post(url, json=data, headers=headers)

        if response.status_code != 200:
            raise errors.RefreshTokenFailedError

        # Return oauth_tokens
        return response.json()
