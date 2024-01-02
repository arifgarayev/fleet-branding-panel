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

class VideoUploaderController:

    AZ_CAR_REG_REGEX = r"^\d{2}[A-Z]{2}\d{3}$"
    _applied_car_model_obj: Car # validate_car function sets this value
    _secure_filename: str # save_file_locally function sets this value

    def __init__(
            self,
            car_repository,
            request,
            applications_repo
            ):


        self.car_repository = car_repository
        self.request = request


        try:
            self.req_car_reg_input_t = int(self.request.form['isCustomCarReg'])

        except:
            self.req_car_reg_input_t = 1



        if self.req_car_reg_input_t == 1:
            self.custom_car_reg_num_input = self.request.form['customCarRegNumber'].upper()



        self.applications_repo = applications_repo


    def validate_car(self, list_of_car_models):

        is_exist = False

        if self.req_car_reg_input_t == 0:

            for car_model in list_of_car_models:
                if car_model.id == int(
                        self.request.form['car_reg_number']
                ):
                    self._applied_car_model_obj = car_model

                    is_exist = car_model

                    break

        elif self.req_car_reg_input_t == 1:

            # TODO: validate car reg number
            if re.match(
                    self.AZ_CAR_REG_REGEX,
                    self.custom_car_reg_num_input
            ):

                # check if car exists in this company
                is_exist = self.car_repository.find_by_car_reg(
                        self.custom_car_reg_num_input
                )

                if not is_exist:
                    # if not create a new car entry in db and return car
                    # object
                    is_exist = self.car_repository.create_car_by_reg(
                            self.custom_car_reg_num_input,
                            session['company_id_pk']
                    )

                else:

                    if is_exist.company_id_fkey != session['company_id_pk']:

                        is_exist = self.car_repository.create_car_by_reg(
                                self.custom_car_reg_num_input,
                                session['company_id_pk']
                        )


                self._applied_car_model_obj = is_exist

        return is_exist



    def validate_file(self):
        return True if 'file' in list(self.request.files.keys())[0] else False



    async def add_new_record_for_application(self, folder_uuid, filename, type_of_application=2):
        # known values: car_id, user_id, quote,
        # create an event loop
        await self.applications_repo.add_new_application(car_id=self._applied_car_model_obj.id,
                                                    user_id=current_user.id,
                                                    type_of_application=type_of_application,
                                                    folder_uuid=folder_uuid,
                                                    filename=filename,
                                                   quote=self.request.form['comment'])


    def put(self, url):
        req = requests.Session()

        uploaded_file = self.file.read()
        req.put(url, data=uploaded_file)
