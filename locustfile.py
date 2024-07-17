from __future__ import annotations
import base64
import json
import random
import re
from locust import HttpUser, task
from requests.auth import HTTPBasicAuth
import time

headers = {
    "Content-Type": "application/json",
}

# 用戶資料列表
teamIds = list(range(1, 251))
userIds = list(range(1, 4))

with open("test.zip", "rb") as pyfile:
    file_content = pyfile.read()
file = base64.b64encode(file_content).decode("utf-8")


class User(HttpUser):
    # @task
    # def login(self):
    #     teamId = random.choice(teamIds)
    #     userId = random.choice(userIds)
    #     user = {"username": f'test_team{teamId}_user{userId}', "password": str(userId) * 10}

    #     # Get CSRF token
    #     login_page = self.client.get("/login")
    #     csrf = re.search(r'<input type="hidden" name="_csrf_token" value="([^"]*)">', login_page.text)

    #     while not csrf:
    #         time.sleep(2)
    #         login_page = self.client.get("/login")
    #         csrf = re.search(r'<input type="hidden" name="_csrf_token" value="([^"]*)">', login_page.text)

    #     csrf_token = csrf.group(1)

    #     # Login
    #     payload = {
    #         "_username": user["username"],
    #         "_password": user["password"] if user["password"] else user,
    #         "_csrf_token": csrf_token
    #     }
    #     login_response = self.client.post("/login", data=payload)

    #     if login_response.status_code == 200:
    #         pass
    #     else:
    #         raise Exception(f"Failed to login, status: {login_response.status_code}, user: {user["username"]}.")
    @task
    def submit(self):
        teamId = random.choice(teamIds)
        userId = random.choice(userIds)
        user = {
            "username": f"test_team{teamId}_user{userId}",
            "password": str(userId) * 10,
        }
        user_auth = HTTPBasicAuth(user["username"], user["password"])

        data = json.dumps(
            {
                "language_id": "python3",
                "problem_id": "1",
                "team_id": teamId * 3 + 2,
                "files": [{"data": file, "mime": "application/zip"}],
            }
        )
        response = self.client.post(
            "/api/v4/contests/1/submissions",
            auth=user_auth,
            data=data,
            headers=headers,
        )

        # Check the response
        if response.status_code in [200, 201]:
            pass
        elif response.status_code == 500:
            print(user)
            raise Exception("Failed:", response.status_code, response.text)
        else:
            raise Exception("Failed:", response.status_code, response.text)
