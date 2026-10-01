import traceback
import sys
import os

def app(environ, start_response):
    try:
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from app.main import app as fastapi_app
        return fastapi_app(environ, start_response)
    except Exception as e:
        status = '500 Internal Server Error'
        headers = [('Content-type', 'text/plain; charset=utf-8')]
        start_response(status, headers)
        error = traceback.format_exc()
        return [error.encode('utf-8')]
