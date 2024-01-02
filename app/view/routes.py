from math import ceil
from app.middlewares.datetime_checker import date
import requests
from flask import Blueprint, jsonify, Response
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from flask import Flask, render_template, request, make_response, redirect, url_for, session, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from flask_cors import CORS
import os
from app.controller.auth import UserController
from app.services.gcp_cloud_storage import VideoUploaderService
from app.view.webforms.login_form import LoginForm
from app.view.auth import user_repository
from dependencies import csrf
from app.view.video_upload import applications_repository


app = Blueprint("api", __name__)




@app.route('/favicon.ico')
def favicon():

    return send_from_directory(os.path.join(app.root_path, '../../static/img'),
                               'favicon.ico')


# keep in common view routes
@app.route('/logout')
@login_required
def logout():
    user = user_repository.find_by_id(current_user.get_id())


    if user:
        logout_user()
    return redirect('/login')


@app.route('/upload_u', methods=['POST'])
@date(request)
@csrf.exempt
def upldddoad():

    filename = request.headers.get('X-File-Name')
    file_size = int(request.headers.get('X-File-Size'))
    current_iter = int(request.headers.get('X-Current-Iter'))
    folder_uuid = str(request.headers.get('X-UUID'))

    iter_quantity = int(ceil(file_size / (1024 * 1024) / 30))



    # print(folder_uuid)
    if current_iter == 1:
        try:
            os.mkdir(os.environ.get('GOOGLE_STORAGE_LOCAL_DEST') + f'/{folder_uuid}')
        except FileExistsError:
            pass

    with open(os.environ.get('GOOGLE_STORAGE_LOCAL_DEST') + f'/{folder_uuid}/{filename}', 'ab') as f:
        while True:
            chunk = request.stream.read(1024 * 1024 * 30)
            if not chunk:
                break
            f.write(chunk)

    if iter_quantity == current_iter:

        session['folder'] = folder_uuid
        session['filename'] = filename

        return 'File uploaded successfully'

    return 'Waiting for another chunk'



