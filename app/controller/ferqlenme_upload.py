import os
import re

import requests

from .auth import session, current_user
from werkzeug.utils import secure_filename
from config.default import UPLOAD_FOLDER
from app.model.cars import Car
import uuid
from dependencies import bucket, executor, pprocess
from app.services.gcp_cloud_storage import VideoUploaderService
from app.view.auth import current_user


class FerqlenmeUploaderController:
    AZ_CAR_REG_REGEX = r"^\d{2}[A-Z]{2}\d{3}$"
    _applied_car_model_obj: Car  # validate_car function sets this value
    _secure_filename: str  # save_file_locally function sets this value\
    DISALLOWED_EXTENSIONS = {"mp4", "avi", "mkv", "mov"}

    def __init__(self, car_repository, request, applications_repo):
        self.car_repository = car_repository
        self.request = request
        self.folder_uuid = str(uuid.uuid4())
        self.applications_repo = applications_repo
        self.file = self.request.files["video_file"]
        self.gcp_video_uploader = VideoUploaderService(
            str(secure_filename(self.file.filename)), self.folder_uuid
        )

        try:
            self.req_car_reg_input_t = int(self.request.form["isCustomCarReg"])

        except:
            self.req_car_reg_input_t = 1

        if self.req_car_reg_input_t == 1:
            self.custom_car_reg_num_input = self.request.form[
                "customCarRegNumber"
            ].upper()

    def validate_car(self, list_of_car_models) -> Car or bool:
        is_exist = False

        if self.req_car_reg_input_t == 0:
            for car_model in list_of_car_models:
                if car_model.id == int(self.request.form["car_reg_number"]):
                    self._applied_car_model_obj = car_model

                    is_exist = car_model

        elif self.req_car_reg_input_t == 1:
            # TODO: validate car reg number
            if re.match(self.AZ_CAR_REG_REGEX, self.custom_car_reg_num_input):
                # check if car exists in this company
                is_exist = self.car_repository.find_by_car_reg(
                    self.custom_car_reg_num_input
                )

                if not is_exist:
                    # if not create a new car entry in db and return car
                    # object
                    is_exist = self.car_repository.create_car_by_reg(
                        self.custom_car_reg_num_input, session["company_id_pk"]
                    )

                self._applied_car_model_obj = is_exist

        return is_exist

    def disallowed_file(self, filename):
        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower() in self.DISALLOWED_EXTENSIONS
        )

    def validate_file(self):
        return (
            True
            if "file" in list(self.request.files.keys())[0]
            and not self.disallowed_file(self.file.filename)
            else False
        )

    def save_file_locally(self):
        return self.folder_uuid, str(secure_filename(self.file.filename))
        # self._secure_filename = str(secure_filename(self.request.files[
        # 'video_file'].filename))
        # return self.folder_uuid, secure_filename(self.request.files[
        # 'video_file'].filename)

    async def add_new_record_for_application(self, filename, type_of_application=1):
        # known values: car_id, user_id, quote,
        # create an event loop
        await self.applications_repo.add_new_application(
            car_id=self._applied_car_model_obj.id,
            user_id=current_user.id,
            type_of_application=type_of_application,
            folder_uuid=self.folder_uuid,
            filename=filename,
            quote=self.request.form["comment"],
        )

    def push_file_to_cloud_async(self):
        # pprocess.submit(gcp_video_uploader.upload_to_cloud)
        self.gcp_video_uploader.upload_to_cloud(self.file)

    def generate_signed_url(self):
        # TODO
        return self.gcp_video_uploader.generate_signed_urls_post()

    def put(self, url):
        req = requests.Session()

        uploaded_file = self.file.read()
        req.put(url, data=uploaded_file)
