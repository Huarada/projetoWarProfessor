import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from main import app

def application(environ, start_response):
    # Corrige crash do EB quando não existe CONTENT_LENGTH
    if 'CONTENT_LENGTH' not in environ or environ['CONTENT_LENGTH'] == '':
        environ['CONTENT_LENGTH'] = '0'
    return app.wsgi_app(environ, start_response)
