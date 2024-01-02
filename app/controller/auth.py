from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, current_user
from flask import session, jsonify
from dependencies import bcrypt
from datetime import datetime
import pytz


class UserController:

    def __init__(self, user_model, user_repository):
        self.user_model = user_model
        self.user_repository = user_repository

        # print("Inside UserController object: ", user_model.password)


    def set_session(self,
                    session_name : str,
                    session_data):

        session[session_name] = session_data

    def validate_username_and_password(self, user_input_password, user_input_username) -> bool:


        # self.user_model = True <- already checks if user exists or not
        if self.user_model and bcrypt.check_password_hash(self.user_model.password,
                                                          user_input_password) and len(user_input_password) < 50 and self.validate_username(user_input_username):

            # baku_timezone_now = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Baku'))
            #
            # if not self.user_model.is_admin and baku_timezone_now.weekday() > 4:
            #
            #     return False


            login_user(self.user_model)

            comnpany_joined_model = self.user_repository.join_with_company(current_user.id)


            session['company_id_pk'] = comnpany_joined_model.id
            session['internal_company_name'] = comnpany_joined_model.internal_company_name
            session['internal_company_status'] = comnpany_joined_model.internal_company_status
            session['internal_company_balance_ref'] = comnpany_joined_model.internal_company_balance_ref
            session['is_admin'] = self.user_model.is_admin
            session['all_user_roles'] = [int(i.role_fkey) for i in self.user_repository.get_all_user_roles(
                self.user_model.id
            )]
            # session["keyword"] = [
            #     {}
            # ]




            # print(session['all_user_roles'])


            #TODO user-related global session values added here
            





            return True

        return False

    def validate_username(self, user_input_username):

        # self.user_model = True <- already checks if user exists or not
        if self.user_model and len(user_input_username) < 50 and not user_input_username.isdigit():
            return True

        return False


