# Cotter Login SDK for Python CLI

Cotter's Python SDK for Passwordless Authentication using Email/Phone Number for your CLI and scripts.
To read more about Cotter, get started with our 📚 integration guides and example projects.

**Find the most updated documentation on our site or our Github:**

- [Documentation](https://docs.cotter.app/sdk-reference/python-for-cli)
- [Github](https://github.com/cotterapp/python-sdk)

# Installation

```
pip install cotter
```

Find the latest versions here https://pypi.org/project/cotter/

# Usage

Get your `API_KEY_ID` from [Cotter's Dashboard](https://dev.cotter.app).

### Step 1: Copy [`cotter_login_success.html`](https://github.com/cotterapp/python-sdk/blob/master/example/cotter_login_success.html) from the `example` folder.

You can make your own Success page. After the user successfully logged-in, the website will redirect to `http://localhost:port` and you should show a "Success message" and tell the user to go back to your terminal. Feel free to copy our example page and modify it.

**Put the success page with name `cotter_login_success.html` at the same directory as where you put the code below**

### Step 2: Call Cotter's login function

```python
import cotter
api_key = "YOUR API KEY ID"
port = 8080 # Open a port to receive code from the website after successful authentication
response = cotter.login_with_email_link(api_key, port)
print(response)
```

# Available methods:

### Using Email

```python
# Use Magic Link
response = login_with_email_link(api_key, port)
# Use OTP
response = login_with_email_otp(api_key, port)
```

### Using Phone Number

```python
# Use Magic Link
response = login_with_phone_link(api_key, port)
# Use OTP
response = login_with_phone_otp(api_key, port)
```

# Storing the tokens 

### Store the tokens to a file:
```python
from cotter import tokenhandler
tokenhandler.store_token_to_file(response["oauth_token"], "cottertoken.json")
```
### Get the tokens to a file (automatically refresh if needed):
```python
from cotter import tokenhandler
oauth_token = tokenhandler.get_token_from_file("cottertoken.json", api_key)
```

# Refreshing tokens (if not using the functions above)
```python
# This will only refresh if needed
from cotter import tokenhandler
oauth_token = tokenhandler.refresh_token(oauth_token, api_key)
```

# Validating tokens
```python
from cotter import validate
access_token_decoded = validate.validate_access_token(response["oauth_token"]["access_token"], api_key)
id_token_decoded = validate.validate_id_token(response["oauth_token"]["id_token"], api_key)
```

# Troubleshooting

### Allowed Origin Error

If you get an error like this:

```javascript
{
  "msg": "The redirect URL http://localhost:1234 or the parent origin :// is not in the list of allowed URLs. Please contact the site owner.",
  "type": ""
}
```

You may have set up a list of Allowed URLs in the dashboard. Make sure you add these 2 urls:

- `http://localhost:<PORT>` based on the port you used above
- `://` (this is a bug, join our [Slack channel](https://join.slack.com/t/askcotter/shared_invite/zt-dxzf311g-5Mp3~odZNB2DwYaxIJ1dJA) to be updated)
