import requests
from requests.auth import HTTPBasicAuth

def submit(user, password, data):
    user_auth = HTTPBasicAuth(user, password)

    # Make the request with basic auth
    response = requests.post("/api/v4/contests/1/submissions", auth = user_auth, data = json.dumps(data), headers = headers)
    
    # Check the response
    if response.status_code in [200, 201]:
        print('Success:', response.json())
        return response.json()
    else:
        raise Exception('Failed:', response.status_code, response.text)
