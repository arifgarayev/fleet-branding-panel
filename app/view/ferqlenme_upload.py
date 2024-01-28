import asyncio

from flask import Blueprint, jsonify
from flask_wtf import csrf
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from flask import (
    Flask,
    render_template,
    request,
    make_response,
    redirect,
    url_for,
    session,
    send_from_directory,
)
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    UserMixin,
    current_user,
)
from flask_cors import CORS
import os
from app.controller.auth import UserController
from app.repository.applications import ApplicationsRepository
from app.services.gcp_cloud_storage import VideoUploaderService
from dependencies import csrf, io_loop, pprocess
from app.view.auth import user_repository
from app.repository.company import CompanyRepository
from app.repository.cars import CarRepository
from app.model.cars import Car
from app.controller.ferqlenme_upload import FerqlenmeUploaderController
from app.view.video_upload import (
    car_repository,
    company_repository,
    applications_repository,
)
from app.middlewares.datetime_checker import date


app = Blueprint("ferqlenme_upload", __name__)


@app.route("/ferqlenme-upload", methods=["GET", "POST"])
@login_required
@date(request)
@csrf.exempt
def ferqlenme_upload():
    title = "Fərqlənmə nişanı"

    all_cars: list[Car] = car_repository.get_all_company_cars(session["company_id_pk"])

    if all_cars and request.method == "POST":
        this_controller = FerqlenmeUploaderController(
            car_repository, request, applications_repository
        )

        signed_put_url = this_controller.generate_signed_url()

        if this_controller.validate_car(all_cars) and this_controller.validate_file():
            is_uploaded_locally = (
                this_controller.save_file_locally()
            )  # returs bool or tuple -> folder_uuid, filename

            if is_uploaded_locally:
                # gcp_video_uploader = VideoUploaderService(is_uploaded_locally[1], is_uploaded_locally[0])

                # this_controller.push_file_to_cloud_async()

                # pprocess.submit(this_controller.push_file_to_cloud_async)
                # this_controller.push_file_to_cloud_async()
                this_controller.put(signed_put_url)

                # async

                io_loop.run_until_complete(
                    this_controller.add_new_record_for_application(
                        is_uploaded_locally[1]
                    )
                )

                # io_loop.run(this_controller.add_new_record_for_application(is_uploaded_locally[1]))

                # return success message

                return render_template(
                    "./index/ferqlenme_upload_form.html",
                    title=title,
                    fleet_name=session["internal_company_name"],
                    internal_company_balance_ref=session[
                        "internal_company_balance_ref"
                    ],
                    all_cars=all_cars,
                    is_uploaded=True,
                    keyword=session["keyword"],
                )

            else:
                return render_template(
                    "./index/ferqlenme_upload_form.html",
                    title=title,
                    fleet_name=session["internal_company_name"],
                    internal_company_balance_ref=session[
                        "internal_company_balance_ref"
                    ],
                    all_cars=all_cars,
                    is_uploaded=False,
                    keyword=session["keyword"],
                )
                # render template -> send fail message

        else:
            return render_template(
                "./index/ferqlenme_upload_form.html",
                title=title,
                fleet_name=session["internal_company_name"],
                internal_company_balance_ref=session["internal_company_balance_ref"],
                all_cars=all_cars,
                is_uploaded=False,
                keyword=session["keyword"],
            )
            # return error message

    # GET request
    return render_template(
        "./index/ferqlenme_upload_form.html",
        title=title,
        fleet_name=session["internal_company_name"],
        internal_company_balance_ref=session["internal_company_balance_ref"],
        all_cars=all_cars,
        keyword=session["keyword"],
    )
