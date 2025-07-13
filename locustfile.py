from __future__ import annotations
import base64
import random
import re
from locust import HttpUser, task, constant
import json
from requests.auth import HTTPBasicAuth

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

headers_json = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Content-Type": "application/json",
}

# 用戶資料列表
teamIds = list(range(1, 251))
userIds = list(range(1, 4))

pages = [
    "/team/problems",
    "/team/problems/1/statement",
    "/team/problems/2/statement",
    "/team/problems/3/statement",
]

with open("test.zip", "rb") as pyfile:
    file_content = pyfile.read()
file = base64.b64encode(file_content).decode("utf-8")


class User(HttpUser):
    wait_time = constant(3)

    def on_start(self):
        self.teamId = random.choice(teamIds)
        self.userId = random.choice(userIds)

        self.user = {
            "username": f"test_team{self.teamId}_user{self.userId}",
            "password": str(self.userId) * 10,
        }
        self.user_auth = HTTPBasicAuth(self.user["username"], self.user["password"])
        self.data = json.dumps(
            {
                "language_id": "cpp",
                "problem_id": "1",
                "team_id": self.teamId + 2,
                "files": [{"data": file, "mime": "application/zip"}],
            }
        )

        # Get CSRF token
        login_page = self.client.get("/login", headers=headers, verify=False)
        csrf = re.search(
            r'<input type="hidden" name="_csrf_token" value="([^"]*)">', login_page.text
        )
        login = re.search(r"<title>(.*?) - DOMjudge</title>", login_page.text)

        if login:
            self.client.get("/logout", headers=headers, verify=False)
        elif csrf:
            csrf_token = csrf.group(1)

            # Login
            payload = {
                "_username": self.user["username"],
                "_password": (
                    self.user["password"] if self.user["password"] else self.user
                ),
                "_csrf_token": csrf_token,
            }
            login_response = self.client.post("/login", headers=headers, data=payload, verify=False)
            if login_response.status_code == 200:
                pass
            else:
                raise Exception(
                    f"Failed to login, status: {login_page.status_code}, user: {self.user['username']}."
                )

    def on_stop(self):
        # Get CSRF token
        login_page = self.client.get("/login", headers=headers, verify=False)
        login = re.search(r"<title>(.*?) - DOMjudge</title>", login_page.text)

        if login:
            self.client.get("/logout", headers=headers, verify=False)

    @task(60)
    def view_scoreboard(self):
        scoreboard = self.client.get("/team/scoreboard", headers=headers, verify=False)
        title = re.search(r"<title>(.*?) - DOMjudge</title>", scoreboard.text)

        if scoreboard.status_code == 200 and title:
            pass
        else:
            print(title)
            raise Exception(
                f"Failed to view scoreboard, status: {scoreboard.status_code}, user: {self.user['username']}."
            )

    @task(3)
    def submit(self):
        submission = self.client.post(
            "/api/v4/contests/1/submissions",
            auth=self.user_auth,
            data=self.data,
            headers=headers_json,
            verify=False,
        )

        # Check the response
        if submission.status_code in [200, 201]:
            pass
        else:
            raise Exception("Failed:", submission.status_code, submission.text)

    @task(5)
    def others(self):
        page = random.choice(pages)
        info = self.client.get(page, headers=headers, verify=False)
        title = re.search(r"<title>(.*?) - DOMjudge</title>", info.text)

        if info.status_code == 200 and title:
            pass
        else:
            print(title)
            raise Exception(
                f"Failed to view scoreboard, status: {info.status_code}, user: {self.user['username']}."
            )
