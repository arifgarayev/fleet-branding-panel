import time
from app.model.user_roles import UserRoles
from app.model.user import User, db

class UserRepository:

    _session = None
    def find_by_username(self, username):
        return self._session.query(User).filter_by(username=username).first()

    def find_by_id(self, id) -> User:
        # print("I AM FIND BY ID and MY ID IS: ", id)
        return self._session.query(User).get(id)


    def join_with_company(self, id):
        user = self._session.query(User).filter_by(id=id).first()
        return user.users_company_id_fk


    def get_user_by_company_fkey(self, company_id_fkey):

        return self._session.query(User).filter_by(company_id_fkey=company_id_fkey).first()

    def set_session(self, db_session):
        if db_session:
            self._session = db_session


    def get_all_users(self):

        return self._session.query(User).all()

    def does_exist(self, username):
        return self._session.query(User).filter_by(
            username=username
        ).all()
    def create_a_user(self, user_model):

        self._session.add(user_model)

        self._session.commit()

        return user_model


    def get_all_user_roles(self,
                       user_id):

        return self._session.query(
            UserRoles
        ).filter(
            UserRoles.user_fkey == user_id
        ).all()