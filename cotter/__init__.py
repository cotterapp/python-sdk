
import requests
import webbrowser
import base64
import os
import hashlib
import socket
import time
import sys
import random
import string
from http.server import BaseHTTPRequestHandler, HTTPServer

try:
    import urlparse
    from urllib import urlencode
except:  # For Python 3
    import urllib.parse as urlparse
    from urllib.parse import urlencode
try:
    from urlparse import parse_qsl
except ImportError:
    from urllib.parse import parse_qsl


__author__ = "Putri Karunia"


def url_encoder(url, params):
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)

    url_parts[4] = urlencode(query)

    return urlparse.urlunparse(url_parts)


class ClientRedirectServer(HTTPServer):
    """A server to handle OAuth 2.0 redirects back to localhost.
    Waits for a single request and parses the query parameters
    into query_params and then stops serving.
    """
    query_params = {}


class ClientRedirectHandler(BaseHTTPRequestHandler):
    """A handler for OAuth 2.0 redirects back to localhost.
    Waits for a single request and parses the query parameters
    into the servers query_params and then stops serving.
    """
    def do_GET(s):
        """Handle a GET request.
        Parses the query parameters and prints a message
        if the flow has completed. Note that we can't detect
        if an error occurred.
        """
        f = open('cotter_login_success.html', 'rb')
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        query = s.path.split('?', 1)[-1]
        query = dict(parse_qsl(query))
        s.server.query_params = query
        s.wfile.write(f.read())

    def log_message(self, format, *args):
        """Do not log messages to stdout while running as command line program."""
        pass


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def get_access_token(api_key, code, challenge_id, code_verifier, redirect_url):
    url = 'https://www.cotter.app/api/v0/verify/get_identity?oauth_token=true'
    headers = {'Content-Type': 'application/json', 'API_KEY_ID': api_key}
    data = {
        "code_verifier": code_verifier.decode("utf-8"),
        "authorization_code": code,
        "challenge_id": int(challenge_id),
        "redirect_url": redirect_url
    }
    response = requests.post(url, json=data, headers=headers)

    if response.status_code != 200:
        response.raise_for_status()

    return response.json()


def login(api_key, port, identity_type, auth_method):
    state = get_random_string(10)

    # Generate Code Challenge and Code Verfiier
    verifier_bytes = os.urandom(32)
    code_verifier = base64.urlsafe_b64encode(verifier_bytes).rstrip(b'=')
    challenge_bytes = hashlib.sha256(code_verifier).digest()
    code_challenge = base64.urlsafe_b64encode(challenge_bytes).rstrip(b'=')

    # Prompt user to login at the web browser
    redirect_url = 'http://localhost:' + str(port)
    url = "https://js.cotter.app/app"
    params = {
        'api_key': api_key,
        'redirect_url': redirect_url,
        'state': state,
        'code_challenge': code_challenge,
        'type': identity_type,
        'auth_method': auth_method
    }
    full_url = url_encoder(url, params)
    webbrowser.open(full_url)
    print("Open this link to login at your browser: " + full_url)

    # Listen for redirect from browser with authorization code
    httpd = ClientRedirectServer(('localhost', port), ClientRedirectHandler)
    httpd.handle_request()
    if 'error' in httpd.query_params:
        sys.exit('Authentication request was rejected.')
    if 'code' in httpd.query_params:
        code = httpd.query_params['code']
        state = httpd.query_params['state']
        challenge_id = httpd.query_params['challenge_id']
        return get_access_token(api_key, code, challenge_id,
                                code_verifier, redirect_url)
    else:
        print('Failed redirecting after authentication.')


def login_with_email_link(api_key, port):
    return login(api_key, port, "EMAIL", "MAGIC_LINK")


def login_with_email_otp(api_key, port):
    return login(api_key, port, "EMAIL", "OTP")


def login_with_phone_link(api_key, port):
    return login(api_key, port, "PHONE", "MAGIC_LINK")


def login_with_phone_otp(api_key, port):
    return login(api_key, port, "PHONE", "OTP")
