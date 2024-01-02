from app.model.applications import Applications
from app.model.cars import Car
from app.model.company import Company
from sqlalchemy import func, update


class ApplicationsRepository:

    _session = None
    _async_session = None

    def find_application_by_id(self, id):
        return self._session.query(Applications).filter_by(id=id) \
            .first()


    def get_all_company_applications(self, company_id):
        #  applications = Application.query.join(Car).join(Company).filter(Company.id == company_id).all()
        #     return applications
        return self._session.query(Applications).join(Car).join(Company).filter(Company.id == company_id, Applications.is_archived == 0).order_by(Applications.date_applied.desc()).all()


    def get_all_applications_bulk(self, limit : int, offset: int, is_superuser=None):
        if limit >= 0:
            if not is_superuser:
                return self._session.query(Applications).join(Car).join(Company).filter(Applications.is_archived == 0).order_by(Applications.application_status.desc(), Applications.date_applied.asc()).offset(offset).limit(limit).all()

            else:
                return self._session.query(Applications).join(Car).join(Company).order_by(Applications.application_status.desc(),
                                                            Applications.date_applied.asc()).offset(offset).limit(
                    limit).all()

        else:
            return self._session.query(Applications).join(Car).join(Company).order_by(
                Applications.application_status.desc(),
                Applications.date_applied.asc()).all()


    async def add_new_application(self, car_id, user_id, type_of_application, folder_uuid, filename, quote, is_requested_to_delete=0):


        # async with self._async_session() as session:

        if folder_uuid and filename:
            self._session.add(Applications(type_of_application=int(type_of_application),
                                   folder_uuid=str(folder_uuid),
                                   quote=str(quote),
                                   filename=str(filename),
                                   users_id_fkey=int(user_id),
                                   car_id_fkey=int(car_id)))
        else:
            self._session.add(Applications(type_of_application=int(type_of_application),
                                     quote=str(quote),
                                     users_id_fkey=int(user_id),
                                     car_id_fkey=int(car_id),
                                     is_requested_to_delete=int(is_requested_to_delete)))

        self._session.commit()


    def get_application_count(self,
                              is_superuser):

        if not is_superuser:
            return self._session.query(func.count(Applications.id).filter(Applications.is_archived == 0)).all()

        else:
            return self._session.query(func.count(Applications.id)).all()

    def get_pending_applications_count(self):
        return len(self._session.query(Applications.id).filter(Applications.application_status == "Pending",
                                                               Applications.is_archived == 0).all())


    def set_session(self, db_session):
        if db_session:
            self._session = db_session


    def udpate_status(self, application_id, is_accepted=None, is_declined=None, is_revert=None, is_archived=None, car_repo=None):

        application = list_of_archived_applications = None

        if is_accepted:
            application = self.approve_or_decline_or_revert(application_id, "Approved")

            if int(self.get_type_of_application(application_id)) == 3:

                car_id_of_deleted_car = self.get_car_id_from_application_id(application_id)

                # get car ID from application ID, keep it DONE

                car_repo.update_car_internal_status(int(car_id_of_deleted_car), 'deleted')

                # set car status to deleted DONE


        if is_declined:
            application = self.approve_or_decline_or_revert(application_id, "Declined")

        if is_revert:
            application = self.approve_or_decline_or_revert(application_id, "Pending")

        if is_archived:
            list_of_archived_applications = list()
            for elem in application_id:
                list_of_archived_applications.append(self.archive(int(elem)))

        return application or list_of_archived_applications


    def get_car_id_from_application_id(self, application_id):

        return (self._session.query(Applications).filter(Applications.id == application_id).first()).car_id_fkey


    def archive(self, application_id):

        application = self._session.query(Applications).\
            filter(Applications.id == application_id).first()

        application.is_archived = 1

        self._session.commit()

        return application

    def get_type_of_application(self, application_id):

        return (self._session.query(Applications).
                filter(Applications.id == application_id).first()).type_of_application




    def approve_or_decline_or_revert(self, application_id, keyword):
        application = self._session.query(Applications).filter(Applications.id == application_id).first()

        application.application_status = keyword

        self._session.commit()

        return application


    def update_applications_car(self, car_id_pkey, application_id, user_model):

        application = self._session.query(Applications).filter(Applications.id == application_id).first()

        application.car_id_fkey = car_id_pkey


        # get company's user

        application.users_id_fkey = user_model.id



        self._session.commit()

    def update_comment(self, application_id, comment):

        application = self._session.query(Applications).filter(Applications.id == application_id).first()

        application.b_comment = comment

        self._session.commit()


    def search_car_reg_like(self, car_reg, is_superuser=None):
        if is_superuser:
            return self._session.query(Applications).join(Car).join(Company).filter(Car.internal_car_reg_number.like(car_reg)).\
            order_by(Applications.date_applied.desc()).all()

        return self._session.query(Applications).join(Car).join(Company).filter(Applications.is_archived == 0,
                                                                                Car.internal_car_reg_number.like(car_reg)).\
            order_by(Applications.date_applied.desc()).all()


    def archive_all_applications(self):

        self._session.query(Applications).filter(Applications.is_archived == 0).update({Applications.is_archived: 1},
                                                                                       synchronize_session=False)

        self._session.commit()


    def get_all(self):

        return self._session.query(Applications).all()