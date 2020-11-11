import json
import os
import random
import string

import django
from django.utils.text import slugify


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "starnavi.settings")
django.setup()


from django.contrib.contenttypes.models import ContentType

from accounts.models import User
from articles.models import Post
from communication.models import LikeDislike


content_type = ContentType.objects.get(model="post")

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


def random_word(string_length: int) -> str:
    """Generate a random word"""
    letters = string.ascii_letters
    return "".join(random.choice(letters) for i in range(string_length))


users_list = []
for user_item in range(users_count):
    users_list.append(
        User(
            username=random_word(random.randint(8, 12)),
            password=random_word(random.randint(8, 12)),
            email=random_word(random.randint(8, 12))
            + "@"
            + random.choice(DOMAINS),
        )
    )
User.objects.bulk_create(users_list)

posts_list = []
for user in User.objects.all():
    for post_item in range(random.randint(1, max_posts_count + 1)):
        title = "".join(
            random.choice(string.printable)
            for ind in range(random.randint(40, 60))
        )
        slug = slugify(title)
        content = "".join(
            random.choice(string.printable)
            for ind_2 in range(random.randint(400, 600))
        )
        posts_list.append(
            Post(author=user, title=title, slug=slug, content=content)
        )
Post.objects.bulk_create(posts_list)

actioned_posts = []
for user in User.objects.all():
    liked_posts = []
    for action_item in range(max_likes_count):
        post = random.choice(Post.objects.all())
        if post not in liked_posts:
            actioned_posts.append(
                LikeDislike(
                    content_type=content_type,
                    object_id=post.id,
                    user=user,
                    vote=LikeDislike.LIKE,
                )
            )
            liked_posts.append(post)
LikeDislike.objects.bulk_create(actioned_posts)

print(
    f"Created {users_count} users, "
    f"{len(posts_list)} posts "
    f"and {len(actioned_posts)} likes"
)
