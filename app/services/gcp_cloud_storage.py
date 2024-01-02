import os
import uuid
from datetime import timedelta, datetime


# import datetime

from google.cloud.storage import Blob


from config.default import UPLOAD_FOLDER
from dependencies import bucket
import shutil
# from app.view.auto_status import car_repository
# from app.view.auth import user_repository

class VideoUploaderService:

    def __init__(self, secure_filename, local_folder_uuid):
        self.secure_filename = secure_filename
        self.cloud_folder_uuid = local_folder_uuid



    # def upload_to_cloud(self):
    #
    #     # print('Uploading file')
    #
    #     blob = bucket.blob(self.cloud_folder_uuid + '/' + self.secure_filename)
    #
    #     try:
    #         blob.upload_from_file(self.req.files['video_file'])
    #
    #
    #
    #     except Exception as e:
    #         # print('Exception: ', e)
    #         pass

    def upload_to_cloud(self):

        blob : Blob = bucket.blob(self.cloud_folder_uuid + '/' + self.secure_filename)


        try:


            blob.upload_from_filename(UPLOAD_FOLDER + '/' + self.cloud_folder_uuid + '/' + self.secure_filename)

            shutil.rmtree(UPLOAD_FOLDER + f'/{self.cloud_folder_uuid}')

        except Exception as e:
            print('Exception: ', e)
            pass
        # shutil.rmtree(UPLOAD_FOLDER + f'/{self.cloud_folder_uuid}')

    @staticmethod
    def get_signed_urls(applications_obj_model: list, car_repository, user_repository):
        urls = dict()

        for model in applications_obj_model:
            if model.type_of_application == 1 or model.type_of_application == 2:
                try:
                    urls[model] = [
                                    bucket.blob(str(model.folder_uuid) + '/' + str(model.filename)).generate_signed_url(datetime.today() + timedelta(30)),
                                   car_repository.find_by_id(model.car_id_fkey),
                                   user_repository.find_by_id(model.users_id_fkey)
                                    ]
                except:
                    urls[model] = ['No url',
                                   car_repository.find_by_id(model.car_id_fkey),
                                   user_repository.find_by_id(model.users_id_fkey)]
            else:
                urls[model] = ['No url',
                               car_repository.find_by_id(model.car_id_fkey),
                               user_repository.find_by_id(model.users_id_fkey)]

        return urls

    @staticmethod
    def is_file_exists(folder_uuid, filename):
        return bucket.get_blob(folder_uuid + "/" + filename)



    def generate_signed_urls_post(self):
        blob: Blob = bucket.blob(self.cloud_folder_uuid + '/' + self.secure_filename)

        return blob.generate_signed_url(version="v4",
                                        method='PUT',
                                        expiration=timedelta(minutes=30)
                                        )



# if __name__ == "__main__":
#     import os
#     from google.cloud import storage
#
#     os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/Users/arifgarayev/PycharmProjects/branded_car_verification_prod/config/carapplication-311912-c5a0de49dc3f.json"
#     os.environ['GCP_BUCKET_NAME'] = "branded-car-verification"
#     os.environ['GOOGLE_STORAGE_FILES_BUCKET'] = "branded-car-verification"
#
#
#
#     client = storage.Client()
#     bucket = client.bucket(os.environ.get('GCP_BUCKET_NAME'))
#
#     print(bucket.blob('branded-car-verification/WhatsApp Image 2023-03-03 at 16.17.49 (4)-gigapixel-low_res-scale-2_00x.jpeg').generate_signed_url(datetime.today() + timedelta(30)))
#     # def upload_to_cloud():
#     #
#     #     blob: Blob = bucket.blob('xyztevdst' + '/' + 'xyzs')
#     #
#     #     # blob.generate_signed_url(method='POST')
#     #
#     #     try:
#     #         with open("/Users/arifgarayev/Desktop/Screen Recording 2023-03-04 at 2.59.27 AM.mov", mode='rb') as file:
#     #             blob.upload_from_file(file)
#     #
#     #     except Exception as e:
#     #         print('Exception: ', e)
#     #         pass
#     #
#     #
#     # upload_to_cloud()


if __name__ == '__main__':
    from flask_sqlalchemy import SQLAlchemy
    from app.repository.applications import ApplicationsRepository

    applications_repository = ApplicationsRepository()
    db = SQLAlchemy()

    applications_repository.set_session(
        db.session
    )


