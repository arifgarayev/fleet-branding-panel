from dependencies import db




class Roles(db.Model):

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    description = db.Column(db.String)
    role_name = db.Column(db.String)

