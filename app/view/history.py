import asyncio

from flask import Blueprint, jsonify
from flask_wtf import csrf
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from flask import Flask, render_template, request, make_response, redirect, url_for, session, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from flask_cors import CORS
import os
from app.controller.auth import UserController
from app.repository.applications import ApplicationsRepository
from app.services.gcp_cloud_storage import VideoUploaderService
from dependencies import csrf, io_loop
from app.view.auth import user_repository
from app.repository.company import CompanyRepository
from app.repository.cars import CarRepository
from app.model.cars import Car
from app.controller.ferqlenme_upload import FerqlenmeUploaderController
from app.view.video_upload import car_repository, company_repository, applications_repository, user_repository



app = Blueprint("history", __name__)


@app.route("/tarixce")
@login_required
@csrf.exempt
def tarixce():

    title = "Sorğu tarixçəsi"

    all_cars: list[Car] = car_repository.get_all_company_cars(session['company_id_pk'])
    all_applications = applications_repository.get_all_company_applications(session['company_id_pk'])

    urls = VideoUploaderService.get_signed_urls(all_applications, car_repository, user_repository)

    # print(urls)

    user_agent = request.headers.get('User-Agent')

    # GET request
    return render_template("./history/history.html", title=title,
                           fleet_name=session['internal_company_name'],
                           internal_company_balance_ref=session['internal_company_balance_ref'], applications=urls,
                           user_agent=user_agent,
                           keyword=session["keyword"])