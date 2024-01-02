from dependencies import db
from app.model.company import Company


class Car(db.Model):

    __tablename__ = 'cars'


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    internal_car_id = db.Column(db.Integer, nullable=False)
    internal_car_reg_number = db.Column(db.String, nullable=False)
    internal_car_vin_no = db.Column(db.String, nullable=True)
    internal_car_model = db.Column(db.String, nullable=False)
    internal_car_year = db.Column(db.Integer, nullable=False)
    internal_source = db.Column(db.String, nullable=False)
    internal_car_color = db.Column(db.String, nullable=False)
    internal_car_status = db.Column(db.String, nullable=False)
    internal_car_date = db.Column(db.DateTime, default=db.func.now())


    company_id_fkey = db.Column(db.Integer, db.ForeignKey('company.id'))

    cars_company_id_fk = db.relationship(Company, backref='cars')


    def get_id(self):
        return str(self.id)