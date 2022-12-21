from django.urls import path

from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.wsgi import get_wsgi_application
from django.core.asgi import get_asgi_application


from game.consumers import GameConsumer

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path(r'game/<int:game_id>', GameConsumer.as_asgi()),
        ]),
    ),
})
