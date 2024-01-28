import time

from app.model.cars import Car


class CarRepository:
    CONST_CUSTOM_CAR_FIELDS = "CUSTOM CREATED CAR"
    _session = None

    def find_by_car_reg(self, car_reg):
        return (
            self._session.query(Car).filter_by(internal_car_reg_number=car_reg).first()
        )

    def create_car_by_reg(
        self,
        car_reg,
        company_id,
        internal_car_id=0,
        internal_car_model=CONST_CUSTOM_CAR_FIELDS,
        internal_car_year=0,
        internal_source=CONST_CUSTOM_CAR_FIELDS,
        internal_car_color=CONST_CUSTOM_CAR_FIELDS,
        internal_car_status="active",
    ):
        new_car = Car(
            internal_car_id=internal_car_id,
            internal_car_reg_number=car_reg,
            internal_car_model=internal_car_model,
            internal_car_year=internal_car_year,
            internal_source=internal_source,
            internal_car_color=internal_car_color,
            internal_car_status=internal_car_status,
            company_id_fkey=company_id,
        )

        self._session.add(new_car)
        self._session.commit()

        return new_car

    def get_all_similar_car_reg(self, car_reg):
        return (
            self._session.query(Car)
            .filter(Car.internal_car_reg_number.like(car_reg.upper()))
            .all()
        )

    def find_by_id(self, id):
        # print("I AM FIND BY ID and MY ID IS: ", id)
        return self._session.query(Car).get(id)

    def get_all_company_cars(self, company_id):
        return (
            self._session.query(Car)
            .filter(
                Car.company_id_fkey == int(company_id),
                Car.internal_car_status != "deleted",
            )
            .all()
        )

    def get_all_cars(self):
        return (
            self._session.query(Car).order_by(Car.internal_car_reg_number.asc()).all()
        )

    def get_company_fkey_by_car_id(self, car_id):
        # FIXME ERROR IS HERE
        # return company's ID only

        return self._session.query(Car).filter_by(id=car_id).first().company_id_fkey

    def update_car_internal_status(self, car_id, car_status):
        car = self.find_by_id(car_id)

        car.internal_car_status = str(car_status)

        self._session.commit()

        return car

    def set_session(self, db_session):
        if db_session:
            self._session = db_session
