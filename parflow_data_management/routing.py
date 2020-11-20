from .consumers import GeneralConsumer
from django.urls import re_path

channel_routing = [
    re_path(r"ws/data/$", GeneralConsumer.as_asgi()),
]

