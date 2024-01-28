from os import environ
from dotenv import load_dotenv

load_dotenv(".env", override=True)


FLASK_APP = environ.get("FLASK_APP")
FLASK_RUN_HOST = environ.get("FLASK_RUN_HOST")
FLASK_RUN_PORT = environ.get("FLASK_RUN_PORT")
FLASK_DEBUG = environ.get("FLASK_DEBUG")


# Global vars t
DB_NAME = environ.get("DB_NAME")
DB_USER = environ.get("DB_USER")
DB_PASS = environ.get("DB_PASS")
DB_HOST = environ.get("DB_HOST")
DB_PORT = environ.get("DB_PORT")

# App config
# SESSION_PERMANENT = environ.get('SESSION_PERMANENT')
# FLASK_SECRET_KEY = environ.get('FLASK_SECRET_KEY')
# SESSION_TYPE = environ.get('SESSION_TYPE')
# TEMPLATES_AUTO_RELOAD = environ.get('TEMPLATES_AUTO_RELOAD')
SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_DATABASE_URI_ASYNC = environ.get("SQLALCHEMY_DATABASE_URI_ASYNC")
SESSION_FILE_DIR = environ.get("SESSION_FILE_DIR")
UPLOAD_FOLDER = environ.get("UPLOAD_FOLDER")
# SESSION_PROTECTION = environ.get('SESSION_PROTECTION')
GCP_BUCKET_NAME = environ.get("GCP_BUCKET_NAME")
try:
    BCRYPT_LOG_ROUNDS = int(environ.get("BCRYPT_LOG_ROUNDS"))

except:
    BCRYPT_LOG_ROUNDS = None
