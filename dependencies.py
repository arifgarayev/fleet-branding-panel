import asyncio
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from google.cloud import storage
from config.default import GCP_BUCKET_NAME, SQLALCHEMY_DATABASE_URI_ASYNC
from flask_executor import Executor
from concurrent.futures import ThreadPoolExecutor


client = storage.Client()

bucket = client.bucket(GCP_BUCKET_NAME)

db = SQLAlchemy()


bcrypt = Bcrypt()


csrf = CSRFProtect()


executor = Executor()  # thread is default

pprocess = ThreadPoolExecutor(max_workers=1)


db_engine = create_async_engine(SQLALCHEMY_DATABASE_URI_ASYNC, echo=True, future=True)
async_session = sessionmaker(db_engine, class_=AsyncSession)


io_loop = asyncio.new_event_loop()
asyncio.set_event_loop(io_loop)
