from __future__ import annotations

from app.services.gcp_cloud_storage import VideoUploaderService
from app.view.video_upload import (
    car_repository,
    company_repository,
    applications_repository,
    user_repository,
)

# from validate_email import validate_email
from app.model.user import User


class Admin:
    def __init__(self, request):
        self.request = request

    def validate_limit(self, is_superuser):
        try:
            applications_count = applications_repository.get_application_count(
                is_superuser=is_superuser
            )

            if (
                int(self.request.args.get("limit"))
                > int(applications_count[0][0]) // 15
                or int(self.request.args.get("limit")) < 0
            ):
                return False
            else:
                return True

        except:
            return False

    def get_gcloud_urls(self, application_model, car_repo, user_repo):
        return VideoUploaderService.get_signed_urls(
            application_model, car_repo, user_repo
        )

    def is_approve_request(self):
        return self.request.form.get("approve")

    def is_reject_request(self):
        return self.request.form.get("reject")

    def is_revert_request(self):
        return self.request.form.get("revert")

    def is_archive_request(self):
        return self.request.form.get("archive")

    def is_archive_all_request(self):
        return self.request.form.get("archiveAll")

    def update_application_status(
        self,
        is_accepted=None,
        is_declined=None,
        is_revert=None,
        is_archived=None,
        is_archived_all=None,
    ):
        application = None

        if is_accepted:
            application = applications_repository.udpate_status(
                int(self.request.form.get("approve")),
                is_accepted=is_accepted,
                car_repo=car_repository,
            )
            self.set_comment(self.request.form.get("approve"))

        elif is_declined:
            application = applications_repository.udpate_status(
                int(self.request.form.get("reject")), is_declined=is_declined
            )
            self.set_comment(self.request.form.get("reject"))

        elif is_revert:
            application = applications_repository.udpate_status(
                int(self.request.form.get("revert")), is_revert=is_revert
            )
            self.set_comment(self.request.form.get("revert"), is_revert=True)

        elif is_archived:
            # print(self.request.form.getlist('applicationIDs[]'))
            list_of_archived_applications = applications_repository.udpate_status(
                self.request.form.getlist("applicationIDs[]"), is_archived=True
            )
            return list_of_archived_applications

        elif is_archived_all:
            applications_repository.archive_all_applications()

        #  update car and company... FIXME later
        if application:
            # print(self.request.form.get('car_ref_' + str(application.id)))
            company_id_based_on_car_id = car_repository.get_company_fkey_by_car_id(
                int(self.request.form.get("car_ref_" + str(application.id)))
            )
            self.update_appropriate_car(
                int(self.request.form.get("car_ref_" + str(application.id))),
                int(application.id),
                int(company_id_based_on_car_id),
            )

        return application

    def update_appropriate_car(self, car_id_pkey, application_id, company_id_fkey):
        # FIXME get company's User model
        user_model = user_repository.get_user_by_company_fkey(company_id_fkey)

        applications_repository.update_applications_car(
            car_id_pkey, application_id, user_model
        )

    def is_duplicated_application(self):
        ...

    def set_comment(self, application_id, is_revert=None):
        if not is_revert:
            applications_repository.update_comment(
                int(application_id),
                self.request.form.get("admin_comment_" + application_id),
            )
        else:
            applications_repository.update_comment(int(application_id), "")

    def validate_company(self, company_name, company_id, balance_ref):
        if company_name.isascii():
            company_name = company_name.strip()

            company_name = (
                company_name[0:2].upper() + " " + company_name[3:].capitalize()
            )

        else:
            company_name = False

        if company_id.isdigit():
            company_id = int(company_id)

        else:
            company_id = False

        if balance_ref.isdigit():
            balance_ref = int(balance_ref)

        else:
            balance_ref = False

        if (
            company_name is not False
            and company_id is not False
            and balance_ref is not False
        ):
            return company_name, company_id, balance_ref

        return False

    def is_company_already_exists(self, comapany_name):
        return company_repository.get_company_by_name(comapany_name)

    def create_company(self, company_name, company_id, balance_ref):
        company_repository.create_new_company(company_name, company_id, balance_ref)

    @staticmethod
    def get_company_by_id(company_id):
        return company_repository.get_by_internal_company_id(int(company_id))

    @staticmethod
    def get_user_by_id(user_id):
        return user_repository.find_by_id(user_id)

    @staticmethod
    def get_all_available_companies():
        return company_repository.get_all_active_companies()

    @staticmethod
    def map_available_companies_with_users(list_of_all_company_models):
        map = {}

        all_users_fkey = [
            user.company_id_fkey for user in user_repository.get_all_users()
        ]

        for c in list_of_all_company_models:
            map[c.id] = {
                c.internal_company_name: all_users_fkey.count(c.id)
                if c.id in all_users_fkey
                else 0
            }

        return map

    def validate_user_creation(
        self,
        username,
        password,
        company_id,
        email=None,
        mobile=None,
        internal_manager_id=None,
    ) -> str | User:
        if user_repository.does_exist(username.casefold()):
            return "This username already exists in our " "Database"

        try:
            my_user = User(username, password, company_id)

            if email:
                my_user.set_email(email)

            if mobile:
                my_user.set_mobile_no(mobile)

            if internal_manager_id:
                my_user.set_internal_manager_id(internal_manager_id)

        except AssertionError as err:
            return str(err)

        return my_user

    def _email(self, email):
        if "@" in email:
            return True

        return False

    #
    # def _mobile(self, mob):
    #
    #     ...
