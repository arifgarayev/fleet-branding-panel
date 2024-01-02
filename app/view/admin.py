import asyncio
import glob
import functools
from datetime import datetime, timedelta

from flask import Blueprint, jsonify, send_file
from flask_wtf import csrf
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from flask import Flask, render_template, request, make_response, redirect, url_for, session, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from flask_cors import CORS
import os
from app.controller.auth import UserController
from app.controller.admin import Admin
from app.repository.applications import ApplicationsRepository
from app.services.gcp_cloud_storage import VideoUploaderService
from config.default import SQLALCHEMY_DATABASE_URI
from dependencies import csrf, io_loop
import sqlalchemy
from sqlalchemy import create_engine
from app.view.auth import user_repository
from app.repository.company import CompanyRepository
from app.repository.cars import CarRepository
from app.model.cars import Car
from app.controller.ferqlenme_upload import FerqlenmeUploaderController
from app.view.video_upload import car_repository, company_repository, applications_repository, user_repository
import pandas as pd
from app.view.helper.helpers import HelperUtils
from app.model.user import User

app = Blueprint("admin", __name__)


def admin_authorization_required(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        if int(session['is_admin']) == 1:

            return fn(*args, **kwargs)

        else:
            return redirect('/')

        # Set a unique name for the wrapper function

    wrapper.__name__ = f"{fn.__name__}"
    wrapper.__module__ = fn.__module__

    return wrapper


@app.route("/admin/", methods=['GET', 'POST'], strict_slashes=False)
@app.route("/admin", methods=['GET', 'POST'])
@login_required
@csrf.exempt
@admin_authorization_required
def admin_index():

    this_controller = Admin(request)


    is_approved = is_declined = is_revert = is_archived = is_archived_all = list_of_updated_applications = updated_application = None

    if request.method == "POST":

        # print(request.form.get('application-id'))


        this_controller.request = request



        if this_controller.is_approve_request():
            updated_application = this_controller.update_application_status(is_accepted=True)
            is_approved = True



            # return template if approved

        elif this_controller.is_reject_request():
            updated_application = this_controller.update_application_status(is_declined=True)
            is_declined = True

        elif this_controller.is_revert_request():
            updated_application = this_controller.update_application_status(is_revert=True)
            is_revert = True

        elif this_controller.is_archive_request():
            # print(request.form.getlist('applicationIDs[]'))
            list_of_updated_applications = this_controller.update_application_status(is_archived=True)
            # print(request.form.getlist('applicationIDs[]'))
            is_archived = True

        elif this_controller.is_archive_all_request():

            this_controller.update_application_status(is_archived_all=True)
            is_archived_all = True





    if not request.args.get('limit'):
        # print(True)
        # print(url_for('admin.admin_index') + '?limit=1')
        return redirect(url_for('admin.admin_index', limit='0'))
    else:
        limit = request.args.get('limit')

        # if request.args.get('is-approved') == "true":
        #     is_approved = True
        #
        # elif request.args.get('is-rejected') == "true":
        #     is_deleted = True



        # fail or success query string or None

    title = "Admin-Panel"


    # GET validation
    if this_controller.validate_limit(is_superuser=True if 1 in session['all_user_roles']
                                                                                 else None):

        try:
            all_applications = applications_repository.get_all_applications_bulk(15, int(limit) * 15,
                                                                                 is_superuser=True if 1 in session['all_user_roles']
                                                                                 else None)
            applications_count = applications_repository.get_application_count(is_superuser=True if 1 in session['all_user_roles']
                                                                                 else None)

            signed_urls = this_controller.get_gcloud_urls(all_applications, car_repository, user_repository)


        except Exception as e:
            print("Exception: ", e)
            return redirect(url_for('admin.admin_index', limit='0'))



        num_of_pages = int(applications_count[0][0]) // 15

        pending_applications_count = applications_repository.get_pending_applications_count()


        # print(applications_count)



        return render_template('./admin/admin_index_new_table.html', title=title, fleet_name=session['internal_company_name'],
                               internal_company_balance_ref=session['internal_company_balance_ref'], application_count=pending_applications_count, all_applications=all_applications,
                            current_limit=int(request.args.get('limit')), num_of_pages=num_of_pages, signed_urls=signed_urls, action_type=(is_approved, is_declined, is_revert, is_archived, is_archived_all), updated_application=updated_application,
                               list_of_updated_applications=list_of_updated_applications, keyword=session["keyword"])

    return redirect(url_for('admin.admin_index', limit='0'))


@app.route("/admin/create/", methods=['GET'])
@app.route("/admin/create", methods=['GET'])
@login_required
@csrf.exempt
@admin_authorization_required
def admin_create_new_user():

    # API gateway, 3 routes.

    title = "Yeni istifadəçi yarad"

    # isCompany + if isCompany == True, then check comapnyId query parameter to generate HTML success page based \
    # on that company
    # else someError or companyAlreadyExists -> send error message to the user



    list_of_all_companies = Admin.\
        get_all_available_companies()

    map_users_companies = Admin.map_available_companies_with_users(list_of_all_companies)

    # print(list_of_all_companies)

    if request.args.get('isSuccess') == "True":



        if request.args.get('isCompany') == "True":

            return render_template('./admin/admin_create_new_user.html',
                               title=title, fleet_name=session['internal_company_name'],
                               internal_company_balance_ref=session['internal_company_balance_ref'],
                                is_success=True, company_name=
                                HelperUtils.try_or_default(lambda: Admin.get_company_by_id(request.args.get('companyId')).
                                                           internal_company_name,
                                                           ""),
                                company_models=map_users_companies, reversed_keys=list(reversed(list(map_users_companies.keys()))),
                                   keyword=session["keyword"]
                               )


        elif request.args.get('isUser') == "True":

            # IMPORTANT FIXXXXXXXXXXXXX -------------------- user_name - argument
            # FIXME repository getter
            return render_template('./admin/admin_create_new_user.html',
                                   title=title, fleet_name=session['internal_company_name'],
                                   internal_company_balance_ref=session['internal_company_balance_ref'],
                                   is_success=True, user_name=
                                   Admin.get_user_by_id(request.args.get('userId')).username,
                                   company_models=map_users_companies, reversed_keys=list(reversed(list(map_users_companies.keys()))),
                                   keyword=session["keyword"]
                                   )


    elif request.args.get('isSuccess') == "False":

        if request.args.get('isCompany') == "True":

            return render_template('./admin/admin_create_new_user.html',
                               title=title, fleet_name=session['internal_company_name'],
                               internal_company_balance_ref=session['internal_company_balance_ref'],
                                is_success=False, error_message= "Bu şirkət artıq mövcuddur.",
                                company_models=map_users_companies, reversed_keys=list(reversed(list(map_users_companies.keys()))),
                                   keyword=session["keyword"]
                                   )


        elif request.args.get('isUser') == "True":
            return render_template('./admin/admin_create_new_user.html',
                                   title=title, fleet_name=session['internal_company_name'],
                                   internal_company_balance_ref=session['internal_company_balance_ref'],
                                   is_success=False, error_message=request.args.get('errorMsg'),
                                   company_models=map_users_companies, reversed_keys=list(reversed(list(map_users_companies.keys()))),
                                   keyword=session["keyword"]
                                   )






    # isUser + if isUser == True, then check userId query parameter to generate HTML success page based \
    # on that user
    # else someError or companyAlreadyExists -> send error message to the user


    return render_template('./admin/admin_create_new_user.html',
                           title=title, fleet_name=session['internal_company_name'],
                               internal_company_balance_ref=session['internal_company_balance_ref'],
                           company_models=map_users_companies, reversed_keys=list(reversed(list(map_users_companies.keys()))),
                           keyword=session["keyword"]
                           )





@app.route("/admin/create-user/", methods=['POST'])
@app.route("/admin/create-user", methods=['POST'])
@login_required
@csrf.exempt
@admin_authorization_required
def admin_create_new_userr():

    controller = Admin(request)





    # check for return type?

    if (input_ := controller.validate_user_creation(
        request.form.get('username').strip().casefold(),
        request.form.get('password'),
        request.form.get('companyId').strip(),
        request.form.get('email').casefold().strip(),
        request.form.get('mobileNo').strip(),
        request.form.get('internalManagerId').strip()
    )):


        if isinstance(input_, User):

            # repository commits our newly created User model
            user_repository.create_a_user(
                input_
            )

            # return redirect with user details for GET method

            return redirect(url_for(
                'admin.admin_create_new_user',
                isSuccess=True,
                isUser=True,
                userId=input_.get_id()
            ))

        else:


            # return redirct with error message for GET method

            return redirect(url_for(
                'admin.admin_create_new_user',
                isSuccess=False,
                isUser=True,
                errorMsg=input_
            ))




    return redirect(url_for('admin.admin_create_new_user'))





@app.route("/admin/create-company/", methods=['POST'])
@app.route("/admin/create-company", methods=['POST'])
@login_required
@csrf.exempt
@admin_authorization_required
def admin_create_new_company():

    controller = Admin(request)

    if (input_ := controller.validate_company(request.form.get('companyName'),
                                   request.form.get('internalCompanyId'),
                                   request.form.get('balanceRefNumber'))
    ):

        # check if company exists or not, to generate an error message
        company_name, internal_company_id, balance_ref_number = input_

        # print(controller.is_company_already_exists(company_name))

        if not controller.is_company_already_exists(company_name):

            controller.create_company(
                company_name,
                internal_company_id,
                balance_ref_number
            )

            return redirect(url_for('admin.admin_create_new_user',
                                    isSuccess=True,
                                    isCompany=True,
                                    companyId=internal_company_id,
                                    ))

        else:

            return redirect(url_for('admin.admin_create_new_user',
                                    isSuccess=False,
                                    isCompany=True))

    return redirect(url_for('admin.admin_create_new_user',
                            isSuccess=False,
                            isCompany=True))



    # return redirect(url_for('admin.admin_create_new_user'))



@app.route("/admin/add-car/", methods=['GET', 'POST'])
@app.route("/admin/add-car", methods=['GET', 'POST'])
@login_required
@csrf.exempt
@admin_authorization_required
def add_new_car():
    return "add_new_car"


@app.route("/admin/stats/", methods=['GET', 'POST'])
@app.route("/admin/stats", methods=['GET', 'POST'])
@login_required
@csrf.exempt
@admin_authorization_required
def stats():
    return "stats"



@app.route("/admin/search")
@app.route("/admin/search/")
@login_required
@csrf.exempt
@admin_authorization_required
def search():

    x = request.args.get('carreg')


    if x:


        applications_like_car_reg = super_user_wrapper(applications_repository.search_car_reg_like,
                                                       f"%{x.upper()}%")


        if applications_like_car_reg:
            res = {}

            limit = 0

            all_apps = super_user_wrapper(
                applications_repository.get_all_applications_bulk,
                15,
                int(limit) * 15
            )

            # all_apps_dump_limit = 15
            # all_apps_dump_current_offset = 0
            #
            #
            #
            # div, mod = divmod(len(all_apps), all_apps_dump_limit)
            # if mod > 0:
            #     total_pages = div + 1
            # else:
            #     total_pages = div

            while all_apps:

                for enum, like_reg in enumerate(applications_like_car_reg):

                    if like_reg in all_apps:

                        if len(all_apps) > 15:

                            div, mod = divmod(all_apps.index(like_reg), 15)

                            if mod > 0:
                                limit = div + 1
                            else:
                                limit = div


                        app_info = {
                            enum: {
                                'app-id': like_reg.id,
                                'app-car-reg': like_reg.applications_car_id_fk.internal_car_reg_number,
                                'app-company': like_reg.applications_users_id_fk.users_company_id_fk.internal_company_name,
                                'app-type': like_reg.type_of_application,
                                'app-status': like_reg.application_status,
                                'app-applied': like_reg.date_applied
                            }
                        }

                        if not limit in res.keys():
                            res[limit] = app_info
                        else:
                            res[limit][enum] = app_info[enum]

                limit += 1

                if len(all_apps) <= 15:

                    all_apps = super_user_wrapper(
                        applications_repository.get_all_applications_bulk,
                        15,
                        int(limit) * 15
                    )

                else:
                    print(jsonify({'result': res}))
                    return jsonify({'result': res})

            # print(res)

            return jsonify({'result': res})

        else:
            return jsonify({'result': 'No such car application'})

    else:
        return jsonify({'result' : 'No such car application'})



@app.route("/admin/searchCar")
@app.route("/admin/searchCar/")
@login_required
@csrf.exempt
@admin_authorization_required
def search_car():

    x = request.args.get('carreg')

    # print(x)

    if x:

        similar_cars = car_repository.get_all_similar_car_reg(f"%{x.upper()}%")

        # print(similar_cars)

        if similar_cars:


            # print({'result': [{0 : i.internal_car_reg_number,
            #                             1 : i.id} for i in similar_cars]})

            return jsonify({'result': [{0 : i.internal_car_reg_number,
                                        1 : i.id} for i in similar_cars]})

        else:
            return jsonify({'result': 'No such car'})


    else:
        return jsonify({'result' : 'No such car'})





@app.route("/admin/select-car")
@app.route("/admin/select-car/")
@login_required
@csrf.exempt
@admin_authorization_required
def select_car():

    x = request.args.get('selectCar')

    if x:
        all_cars = car_repository.get_all_cars()

        if all_cars:
            res = {}



        else:
            return jsonify({'result': 'No such car'})


    else:
        return jsonify({'result' : 'No such car'})




@app.route("/admin/download-csv")
@app.route("/admin/download-csv/")
@login_required
@csrf.exempt
@admin_authorization_required
def download_csv():


    engine = create_engine(SQLALCHEMY_DATABASE_URI)

    # engine.c
    data = pd.read_sql_query("SELECT * FROM applications JOIN cars c on c.id = applications.car_id_fkey JOIN company c2 on c2.id = c.company_id_fkey;", engine)

    csv_data = data.to_csv(path_or_buf="./tmp/downloaded_files/export.csv", index=False, mode='w')

    engine.dispose()

    return send_file("./tmp/downloaded_files/export.csv")

"""
The view function for  did not return a valid response. The function either returned None or ended without a return statement.
"""


def super_user_wrapper(fn, *args):

    if 1 in session['all_user_roles']:

        if fn.__name__ != "search_car_reg_like":
            return fn(
                -1,
                0,
                is_superuser=True
            )
        else:
            return fn(
                *args,
                is_superuser=True
            )

    else:

        return fn(
            *args
        )

