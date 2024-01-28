from app.model.company import Company
from dependencies import db
from app.model.cars import Car
from app.model.user import User


class Applications(db.Model):
    __tablename__ = "applications"
    # __table_args__ = {'schema': 'public'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_applied = db.Column(db.DateTime, default=db.func.now())
    # DateTime, default=datetime.datetime.utcnow)
    type_of_application = db.Column(db.Integer, nullable=False)
    folder_uuid = db.Column(db.String, nullable=True)
    quote = db.Column(db.String, nullable=True)
    is_archived = db.Column(db.Integer, default=0)
    filename = db.Column(db.String, nullable=True)
    b_comment = db.Column(db.String, nullable=True)
    is_requested_to_delete = db.Column(db.Integer, default=0)
    application_status = db.Column(db.String, default="Pending")

    car_id_fkey = db.Column(db.Integer, db.ForeignKey("cars.id"))
    applications_car_id_fk = db.relationship(Car, backref="cars")

    users_id_fkey = db.Column(db.Integer, db.ForeignKey("users.id"))
    applications_users_id_fk = db.relationship(User, backref="users")

    # company = db.relationship(Company, secondary='cars', uselist=False)

    def get_id(self):
        return str(self.id)

    def get_applied_car_id(self):
        return str(self.car_id_fkey)

    def get_user_id(self):
        return str(self.users_id_fkey)
