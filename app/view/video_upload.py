import asyncio
import glob
import shutil
from app.middlewares.datetime_checker import date
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
from dependencies import csrf, io_loop, pprocess, executor
from app.view.auth import user_repository
from app.repository.company import CompanyRepository
from app.repository.cars import CarRepository
from app.model.cars import Car
from app.controller.video_upload import VideoUploaderController


app = Blueprint("video_upload", __name__)

car_repository = CarRepository()
company_repository = CompanyRepository()
applications_repository = ApplicationsRepository()


@app.route("/video-upload", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
@date(request)
@login_required
@csrf.exempt
def index_video_upload():
    title = "Video reklam"

    all_cars: list[Car] = car_repository.get_all_company_cars(session["company_id_pk"])

    # ensure all_cars non empty
    if request.method == "POST" and (int(request.form["isCustomCarReg"]) or all_cars):

        this_controller = VideoUploaderController(
            car_repository, request, applications_repository
        )

        # signed_put_url = this_controller.generate_signed_url()

        if car_selected := this_controller.validate_car(all_cars):
            while "folder" not in session and "filename" not in session:
                pass

            # this_controller.put(signed_put_url)
            if "folder" in session and "filename" in session:
                try:
                    gcp_video_uploader = VideoUploaderService(
                        session["filename"], session["folder"]
                    )

                    executor.submit(gcp_video_uploader.upload_to_cloud)

                    io_loop.run_until_complete(
                        this_controller.add_new_record_for_application(
                            session["folder"], session["filename"]
                        )
                    )

                    # shutil.rmtree(os.environ.get('GOOGLE_STORAGE_LOCAL_DEST') + f'/{session["folder"]}')

                    del session["folder"]

                    del session["filename"]

                except:
                    ...

                return render_template(
                    "./index/video_upload_form.html",
                    title=title,
                    fleet_name=session["internal_company_name"],
                    internal_company_balance_ref=session[
                        "internal_company_balance_ref"
                    ],
                    all_cars=all_cars,
                    is_uploaded=True,
                    car_selected=car_selected,
                    keyword=session["keyword"],
                )

            else:
                return render_template(
                    "./index/video_upload_form.html",
                    title=title,
                    fleet_name=session["internal_company_name"],
                    internal_company_balance_ref=session[
                        "internal_company_balance_ref"
                    ],
                    all_cars=all_cars,
                    is_uploaded=False,
                    keyword=session["keyword"],
                )

        else:
            return render_template(
                "./index/video_upload_form.html",
                title=title,
                fleet_name=session["internal_company_name"],
                internal_company_balance_ref=session["internal_company_balance_ref"],
                all_cars=all_cars,
                is_uploaded=False,
                keyword=session["keyword"],
            )

    if request.method == "GET":
        files = glob.glob(os.environ.get("GOOGLE_STORAGE_LOCAL_DEST") + "/*")

        if files:
            for i in files:
                folder_uuid = i.split("/")[-1].replace("/", "")
                filename = glob.glob(
                    os.environ.get("GOOGLE_STORAGE_LOCAL_DEST") + f"/{folder_uuid}/*"
                )
                if filename:
                    print(True)

                    filename = filename[0].split("/")[-1].replace("/", "")

                    gcp_video_uploader = VideoUploaderService(filename, folder_uuid)

                    executor.submit(gcp_video_uploader.upload_to_cloud)

                    # this_controller = VideoUploaderController(car_repository, request, applications_repository)

                    io_loop.run_until_complete(
                        applications_repository.add_new_application(
                            2357, 183, 2, folder_uuid, filename, "UNDEFINED"
                        )
                    )

        return render_template(
            "./index/video_upload_form.html",
            title=title,
            fleet_name=session["internal_company_name"],
            internal_company_balance_ref=session["internal_company_balance_ref"],
            all_cars=all_cars,
            keyword=session["keyword"],
        )


# regex for car reg number:  ^\d{2}[A-Z]{2}\d{3}$
