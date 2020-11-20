import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from parflow_data_management.routing import channel_routing

# TODO, parameterize the default?
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            channel_routing
        )
    ),
    # Just HTTP for now. (We can add other protocols later.)
})