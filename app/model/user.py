from flask_login import UserMixin
from dependencies import db, bcrypt
from app.model.company import Company
from validate_email import validate_email


class User(db.Model, UserMixin):

    __tablename__ = 'users'
    # __table_args__ = {'schema': 'public'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    mobile = db.Column(db.String)
    alternative_mobile = db.Column(db.Integer, nullable=True)
    internal_company_manager_id = db.Column(db.String)
    company_id_fkey = db.Column(db.Integer, db.ForeignKey('company.id'))

    users_company_id_fk = db.relationship(Company, backref='users')

    date_added = db.Column(db.DateTime, default=db.func.now())
    is_admin = db.Column(db.Integer, default=0)



    def __init__(self,
                 username,
                 password,
                 company_id_fkey):

        self.set_username(username)

        self.set_password(password)

        self.set_company_id_fkey(company_id_fkey)




    def get_id(self):
        return str(self.id)


    def set_password(self, password):

        length = len(password)
        if length > 6 and length < 50:
            self.password = bcrypt.generate_password_hash(password.encode('utf-8')).decode('utf-8')

        else:
            raise AssertionError('Password must be at least 6 at most 60 chars.')

    def set_username(self, username):

        if not username.isdigit():

            self.username = username.casefold()

        else:

            raise AssertionError('Username must contain characters as well.')



    def set_company_id_fkey(self, company_id_pkey):

        if company_id_pkey and company_id_pkey.isdigit():

            try:
                # becase of casting to int()
                self.company_id_fkey = int(company_id_pkey)
            except:
                raise AssertionError('Company ID must be an intiger')

        else:

            raise AssertionError('Please set company id key.')


    def set_email(self, email):

        if validate_email(email):
            self.email = email

    def set_mobile_no(self,
                      mobile_no):

        if '+' in mobile_no:
            mobile_no = mobile_no.replace('+', '')


        if mobile_no.isdigit():
            self.mobile = mobile_no


    def set_internal_manager_id(self,
                                int_mng_id):

        if int_mng_id.isdigit():


            try:
                # because of casting to int()
                self.internal_company_manager_id = int(int_mng_id)

            except:

                ...