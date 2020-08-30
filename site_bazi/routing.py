from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import catan_game.routing

# print(catan_routing.websocket_urlpatterns)
application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            catan_game.routing.websocket_urlpatterns
        )
    ),
})
