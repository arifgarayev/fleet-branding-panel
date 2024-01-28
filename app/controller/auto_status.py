from app.model.cars import Car
from app.view.auth import current_user


class AutoStatusController:
    _applied_car_model_obj: Car

    def __init__(self, request, applications_repo):
        self.request = request
        self.applications_repo = applications_repo

    async def add_new_record_for_application(
        self, car_id, is_requested_to_delete, type_of_application=3
    ):
        # known values: car_id, user_id, quote,
        # create an event loop
        await self.applications_repo.add_new_application(
            car_id=car_id,
            user_id=current_user.id,
            folder_uuid=None,
            filename=None,
            type_of_application=type_of_application,
            quote=self.request.form["fo_comment_" + str(car_id)],
            is_requested_to_delete=is_requested_to_delete,
        )
