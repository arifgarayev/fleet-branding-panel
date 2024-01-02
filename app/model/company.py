from dependencies import db


class Company(db.Model):

    __tablename__ = 'company'
    # __table_args__ = {'schema': 'public'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    internal_company_name = db.Column(db.String, nullable=False)
    internal_company_id = db.Column(db.Integer, nullable=False)
    internal_company_status = db.Column(db.String, nullable=False)
    internal_company_balance_ref = db.Column(db.Integer)
    date_added = db.Column(db.DateTime, default=db.func.now())


    def get_id(self):
        return str(self.id)

    def get_internal_company_name(self):
        return str(self.internal_company_name)


