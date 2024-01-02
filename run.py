from config.default import *
import json
import os, sys
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from dependencies import db, bcrypt, csrf, executor, async_session
from flask import Flask
from flask_cors import CORS

from app.sessionInterface.custom_session import FileSystemSessionInterface
from app.view.routes import app as routes_bp
from app.view.auth import app as auth_bp, user_repository
from app.view.video_upload import app as video_upload_bp, car_repository
from app.view.ferqlenme_upload import app as ferqlenme_upload_bp
from app.view.auto_status import app as auto_status_bp
from app.view.history import app as history_bp
from app.view.error_handler import app as error_handler_bp, page_not_found

from flask_bcrypt import Bcrypt
from app.view.auth import login_manager
from datetime import timedelta
from flask_sslify import SSLify
from app.view.video_upload import applications_repository

# ----------------------------------------------------------------------------------------------

app_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, app_root)



class Entry:


    def __init__(self):

        self.app, self.login_manager, self.db, self.bcrypt = self.entry_point()




    def run_server(self):

        self.app.run(host=FLASK_RUN_HOST)



    def entry_point(self):

        app = Flask(__name__, static_folder='./static', template_folder='./templates')


        # csrf = CSRFProtect(app)

        # enable this, when app is ready for SSL certificate
        # and all set for production

        # sslify = SSLify(app)


        # app.register_blueprint(error_handler_bp)



        # login manager setup
        login_manager.init_app(app)
        login_manager.session_protection = 'strong'
        login_manager.login_view = '/login'
        login_manager.use_session_for_next = True



        app.config.from_file("./config/flaskconfig.json", load=json.load)
        # app.config['SESSION_COOKIE_SECURE'] = False
        app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)
        app.config.update(GOOGLE_STORAGE_SIGNATURE = {"expiration": timedelta(minutes=20)})
        # app.session_interface = FileSystemSessionInterface(SESSION_FILE_DIR)


        # app.register_error_handler(Exception, page_not_found)

        db.init_app(app)
        csrf.init_app(app)
        bcrypt.init_app(app)
        executor.init_app(app)

        # print(bcrypt._log_rounds)



        with app.app_context():
            db.reflect()
        CORS(app)

        return app, login_manager, db, bcrypt

    def register_blueprints(self):

        self.app.register_blueprint(routes_bp)
        self.app.register_blueprint(auth_bp)
        self.app.register_blueprint(video_upload_bp)
        self.app.register_blueprint(ferqlenme_upload_bp)
        self.app.register_blueprint(auto_status_bp)
        self.app.register_blueprint(history_bp)


        # self.app.register_blueprint(error_handler_bp)

    def inject_dependecies(self, list_of_repos):


        # TODO inject database session for repositories, here
        # objects that are not modified on RunTime (or app initialization)

        for repo in list_of_repos:
            repo.set_session(self.db.session)

            if hasattr(repo, '_async_session'):
                # private attr/prop, but it's PYTHOOOOOOON
                repo._async_session = async_session




if __name__ == '__main__':
    app_entry = Entry()

    app_entry.register_blueprints()

    app_entry.inject_dependecies([user_repository, car_repository, applications_repository])

    db = app_entry.db
    bcrypt = app_entry.bcrypt
    login_manager = app_entry.login_manager


    app_entry.run_server()

    # TODO: NOTES FOR PRODUCTION:
    # change flaskconfig.json SESSION_COOKIE_SECURE (to true when SSL is ready) + SECURITY_CSRF_COOKIE_SECURE to false
    # Fix error pages by its status codes and CSRF-Error exceptions
    # configure SSL certificate

