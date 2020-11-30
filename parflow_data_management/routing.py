from .consumers import RemoteEventConsumer
from django.urls import re_path

channel_routing = [
    re_path(r"ws/data/$", RemoteEventConsumer.as_asgi()),
]
