from .consumers import KeyConsumer
from django.urls import re_path

channel_routing = [
    re_path(r"ws/keygen/$", KeyConsumer.as_asgi()),
]