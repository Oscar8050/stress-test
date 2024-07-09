import re
import requests
from requests.auth import HTTPBasicAuth
import json

admin_username = "admin"
admin_password = "2a4AMh4qatCBti_c"
auth = HTTPBasicAuth(admin_username, admin_password)

base_url = "http://10.217.33.233/domjudge"
headers = {
    'Content-Type': 'application/json',
}    

def login(user, password = None):
    session = requests.Session()

    # Get CSRF token
    login_page = session.get(f"{base_url}/login")
    csrf_token = re.search(r'<input type="hidden" name="_csrf_token" value="([^"]*)">', login_page.text).group(1)

    # Login
    payload = {
        "_username": user,
        "_password": password if password else user,
        "_csrf_token": csrf_token
    }

    login_response = session.post(f"{base_url}/login", data = payload)

    if login_response.status_code == 200:
        print(f"{user} logged in successfully.")
    else:
        raise Exception(f"Failed to login, user: {user}.")

def add_user(data):
    # Make the request with basic auth
    response = requests.post(f"{base_url}/api/v4/users", auth = auth, data = json.dumps(data), headers = headers)
    
    # Check the response
    if response.status_code in [200, 201]:
        print('Success:', response.json())
    else:
        raise Exception('Failed:', response.status_code, response.text)

def add_team(data):
    # Make the request with basic auth
    response = requests.post(f"{base_url}/api/v4/contests/1/teams", auth = auth, data = json.dumps(data), headers = headers)
    
    # Check the response
    if response.status_code in [200, 201]:
        print('Success:', response.json())
        return response.json()
    else:
        raise Exception('Failed:', response.status_code, response.text)
