import json
import requests
import uuid
import random


class API:
    def __init__(self, url_base: str, token: str = ""):
        self.token = token
        self.url_base = url_base
        self.headers = {"Content-Type": "application/json"}
        self.html_response: requests.Response = None

    def get_content(self):
        return dict(json.loads(self.html_response.content.decode("utf-8")))

    def get(self, add_to_url: str):
        self.html_response = requests.get(
            self.url_base + add_to_url, headers=self.headers
        )
        if self.html_response.status_code == 200:
            return self.get_content()

    def post(self, add_to_url: str, json_data: dict):
        self.html_response = requests.post(
            self.url_base + add_to_url, json=json_data, headers=self.headers
        )
        if self.html_response.status_code in (200, 201):
            return self.get_content()


class GroupMeAPI(API):
    def __init__(self, token: str):
        super().__init__("https://api.groupme.com/v3", token)
        self.headers["X-Access-Token"] = self.token

    def get_groups(self):
        return self.get("/groups")

    def get_group_id(self, name: str):
        response = self.get_groups()
        if response:
            for group in response["response"]:
                if group["name"] == name:
                    return group["id"]

    def send_message(self, message: str, group_id: str):
        path = f"/groups/{group_id}/messages"
        message_data = {"message": {"source_guid": str(uuid.uuid4()), "text": message}}
        return self.post(path, message_data)


def main():
    groupme = GroupMeAPI("")
    group_id = "96423169"  # = groupme.get_group_id("Test")
    message = "This is a test messsage."
    groupme.send_message(message, group_id)


main()
