import json
import os
import random
import string
from typing import List

import requests


with open("config_for_bot.json") as f:
    config = json.loads(f.read())

users_count = config["number_of_users"]
max_posts_count = config["max_posts_per_user"]
max_likes_count = config["max_like_per_user"]

DOMAINS = [
    "hotmail.com",
    "gmail.com",
    "aol.com",
    "mail.com",
    "mail.ru",
    "yandex.ru",
    "yandex.ua",
    "ukr.net",
    "mail.kz",
    "yahoo.com",
]

PASSWORD = "password"

PROTOCOL = "http://"
HOST = "127.0.0.1"
PORT = "8001"
BASE_URL = f"{PROTOCOL}{HOST}:{PORT}"

os.environ["NO_PROXY"] = HOST


def random_word(string_length: int) -> str:
    """Generate a random word"""
    letters = string.ascii_letters
    return "".join(random.choice(letters) for i in range(string_length))


def get_access_token(ind: int) -> str:
    """Get access token from user login"""
    response = requests.post(
        f"{BASE_URL}/api/v1/login/",
        json={
            "username": f"user{ind + 1}",
            "password": PASSWORD,
        },
    )
    return response.json()["access"]


def users_create() -> None:
    """Users create"""
    for user_item in range(users_count):
        response = requests.post(
            f"{BASE_URL}/api/v1/registration/",
            json={
                "username": f"user{user_item+1}",
                "password": PASSWORD,
                "first_name": f"name{user_item + 1}",
                "last_name": f"surname{user_item + 1}",
            },
        )
        assert response.status_code == 201


def posts_create() -> List[int]:
    """Posts create"""
    posts_ids = []
    for user_item in range(users_count):
        access_token = get_access_token(user_item)
        for _ in range(random.randint(1, max_posts_count)):
            title = "".join(
                random.choice(string.printable)
                for ind in range(random.randint(40, 60))
            )
            content = "".join(
                random.choice(string.printable)
                for ind in range(random.randint(400, 600))
            )
            response = requests.post(
                f"{BASE_URL}/api/v1/articles/create/",
                json={
                    "title": title,
                    "content": content,
                },
                headers={"Authorization": f"Bearer {access_token}"},
            )
            posts_ids.append(response.json()["id"])
            assert response.status_code == 201
    return posts_ids


def likes_create(posts_ids: List[int]) -> None:
    """Likes create"""
    for user_item in range(users_count):
        access_token = get_access_token(user_item)
        for _ in range(max_likes_count):
            response = requests.post(
                f"{BASE_URL}/api/v1/communication/action/",
                json={
                    "vote": random.choice((-1, 1)),
                    "content_type": "post",
                    "object_id": random.choice(posts_ids),
                },
                headers={"Authorization": f"Bearer {access_token}"},
            )
            assert response.status_code in (201, 400)


if __name__ == "__main__":
    users_create()
    ids = posts_create()
    likes_create(ids)
