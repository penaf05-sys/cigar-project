from mangum import Mangum
from asgiref.wsgi import WsgiToAsgi
from server import app

asgi_app = WsgiToAsgi(app)
handler = Mangum(asgi_app, lifespan="off")
