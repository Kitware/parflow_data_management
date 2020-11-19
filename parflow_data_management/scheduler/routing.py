from .consumers import ClusterExecuteConsumer
from django.urls import re_path

channel_routing = [
    re_path(r"ws/execute/$", ClusterExecuteConsumer.as_asgi()),
]