# Cotter Login SDK for Python CLI
Cotter's Python SDK for Passwordless Authentication using Email/Phone Number for your CLI and scripts. 
To read more about Cotter, get started with our 📚 integration guides and example projects.

- [Documentation](https://docs.cotter.app)
- [Quickstart](https://docs.cotter.app/quickstart-guides/all-guides-and-tutorials)

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