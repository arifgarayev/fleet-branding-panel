import asyncio
from flask import Blueprint, jsonify
from flask_wtf import csrf
from app.middlewares.datetime_checker import date
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from flask import Flask, render_template, request, make_response, redirect, url_for, session, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from flask_cors import CORS
import os
from app.controller.auth import UserController
from app.controller.auto_status import AutoStatusController
from app.repository.applications import ApplicationsRepository
from app.services.gcp_cloud_storage import VideoUploaderService
from dependencies import csrf, io_loop
from app.view.auth import user_repository
from app.repository.company import CompanyRepository
from app.repository.cars import CarRepository
from app.model.cars import Car
from app.controller.ferqlenme_upload import FerqlenmeUploaderController
from app.view.video_upload import car_repository, company_repository, applications_repository



app = Blueprint("auto_status", __name__)







@app.route("/avto-status", methods=['GET', 'POST'],
           strict_slashes=False)
@login_required
@date(request)
@csrf.exempt
def auto_status():

    title = "Avtomobilin statusu"

    all_cars: list[Car] = car_repository.get_all_company_cars(session['company_id_pk'])

    if all_cars and request.method == 'POST':

        this_controller = AutoStatusController(request, applications_repository)


        if request.form['submit']:

            io_loop.run_until_complete(this_controller.add_new_record_for_application(request.form['submit'], 1))


        return render_template("./index/auto_status.html", title=title,
                           fleet_name=session['internal_company_name'],
                           internal_company_balance_ref=session['internal_company_balance_ref'], car_model=all_cars,
                               is_uploaded=True, keyword=session["keyword"])

    # GET request
    return render_template("./index/auto_status.html", title=title,
                           fleet_name=session['internal_company_name'],
                           internal_company_balance_ref=session['internal_company_balance_ref'],
                           keyword=session["keyword"],
                           car_model=all_cars)