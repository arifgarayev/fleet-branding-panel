import json
import os

from flask.sessions import SessionInterface
from flask import session
from werkzeug.datastructures import CallbackDict


class FileSystemSessionInterface(SessionInterface):
    def __init__(self, directory):
        self.directory = directory

    def open_session(self, app, request):
        sid = request.cookies.get(app.session_cookie_name)
        if not sid:
            sid = os.urandom(24).hex()
            return {'_session_id': sid}
        filename = os.path.join(self.directory, sid)
        if not os.path.exists(filename):
            return None
        with open(filename, 'r') as f:
            data = f.read()
        return json.loads(data)

    def save_session(self, app, session, response):
        filename = os.path.join(self.directory, session['_session_id'])
        with open(filename, 'w') as f:
            f.write(json.dumps(session))