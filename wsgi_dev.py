import socket

from config.default import *
import json
import os, sys
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from flask import Flask, redirect
from flask_cors import CORS

from dependencies import db, bcrypt, csrf, executor, async_session

from app.sessionInterface.custom_session import FileSystemSessionInterface
from app.view.routes import app as routes_bp
from app.view.auth import app as auth_bp, user_repository, keyword_repo
from app.view.video_upload import app as video_upload_bp, car_repository
from app.view.ferqlenme_upload import app as ferqlenme_upload_bp
from app.view.auto_status import app as auto_status_bp
from app.view.history import app as history_bp
from app.view.admin import app as admin_bp
from app.middlewares.datetime_checker import app as middleware_bp
from app.view.error_handler import (
    app as error_handler_bp,
    page_not_found,
    not_a_weekday,
)

from flask_bcrypt import Bcrypt
from app.view.auth import login_manager
from datetime import timedelta
from flask_sslify import SSLify
from app.view.video_upload import applications_repository, company_repository

# ----------------------------------------------------------------------------------------------

app_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, app_root)

app = Flask(__name__, static_folder="./static", template_folder="./templates")

login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = "/login"
login_manager.use_session_for_next = True

app.config.from_file("./config/flaskconfig_dev.json", load=json.load)
# app.config['SESSION_COOKIE_SECURE'] = False
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=40)
app.config.update(GOOGLE_STORAGE_SIGNATURE={"expiration": timedelta(minutes=30)})
# app.session_interface = FileSystemSessionInterface(SESSION_FILE_DIR)


# TODO FIXME uncomment in production

# app.register_error_handler(405, not_a_weekday)
# app.register_error_handler(Exception, page_not_found)

# app.register_error_handler(Exception, page_not_found)


# FIXME enable
db.init_app(app)
csrf.init_app(app)
bcrypt.init_app(app)
executor.init_app(app)


@app.route("/testdbpoolconn")
def test_db():
    with app.app_context():
        print("DB SETTINGS: ", db.engine.pool.status())

    return redirect("/")


# FIXME enable
with app.app_context():
    db.reflect()

    # print(db.engine.pool.size())


CORS(app)

app.register_blueprint(routes_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(video_upload_bp)
app.register_blueprint(ferqlenme_upload_bp)
app.register_blueprint(auto_status_bp)
app.register_blueprint(history_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(middleware_bp)
app.register_blueprint(error_handler_bp)

list_of_repos = [
    user_repository,
    car_repository,
    applications_repository,
    company_repository,
    keyword_repo,
]

# TODO inject database session for repositories, here
# objects that are not modified on RunTime (or app initialization)


for repo in list_of_repos:
    repo.set_session(db.session)

    if hasattr(repo, "_async_session"):
        # private attr/prop, but it's PYTHOOOOOOON
        repo._async_session = async_session

if __name__ == "__main__":
    app.run(host=FLASK_RUN_HOST, port=FLASK_RUN_PORT, threaded=True)
