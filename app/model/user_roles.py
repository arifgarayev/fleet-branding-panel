from dependencies import db
from app.model.user import User
from app.model.roles import Roles
from dataclasses import dataclass



class UserRoles(db.Model):

    __tablename__ = 'userRoles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_fkey = db.Column(db.Integer, db.ForeignKey('users.id'))
    role_fkey = db.Column(db.Integer, db.ForeignKey('roles.id'))

    userRoles_users_id_fk = db.relationship(User, backref='user_roles_backref')
    userRoles_roles_id_fk = db.relationship(Roles, backref='roles_user_backref')



    def get_roles(self):
        return self.role_fkey


    def get_user(self):
        return self.user_fkey