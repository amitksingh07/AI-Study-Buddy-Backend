import sys
import os
import traceback

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app.main import app
except Exception as e:
    # If the app fails to import, create a dummy WSGI/ASGI app that returns the error
    async def app(scope, receive, send):
        assert scope['type'] == 'http'
        error_msg = traceback.format_exc()
        
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [
                (b'content-type', b'text/plain'),
            ]
        })
        await send({
            'type': 'http.response.body',
            'body': error_msg.encode('utf-8'),
        })
