import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from parflow_data_management.scheduler import routing as scheduler_routing
from parflow_data_management.transport import routing as transport_routing

# TODO, parameterize the default?
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')

all_routes = scheduler_routing.channel_routing + transport_routing.channel_routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            all_routes
        )
    ),
    # Just HTTP for now. (We can add other protocols later.)
})