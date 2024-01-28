from flask import Blueprint, jsonify, g, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from flask import (
    Flask,
    render_template,
    request,
    make_response,
    redirect,
    url_for,
    send_from_directory,
)
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    UserMixin,
    current_user,
)
from flask_cors import CORS
import os
from dependencies import db
from app.controller.auth import UserController, session
from app.view.webforms.login_form import LoginForm
from app.repository.keywords import KeywordsRepo


from app.repository.user import UserRepository

app = Blueprint("auth", __name__)


user_repository = UserRepository()
login_manager = LoginManager()
keyword_repo = KeywordsRepo()


@login_manager.user_loader
def load_user(user_id):
    try:
        return user_repository.find_by_id(user_id)

    except:
        return None


@app.route("/login", methods=["GET", "POST"])
def login():
    # print('DB SETTINGS: ', db.metadata)
    # print('DB SETTINGS: ', db.engines)

    title = "Giriş"

    login_form = LoginForm()

    if login_form.validate_on_submit():
        # user = user_repository.find_by_username(
        #     request.form['username'].lower())

        try:
            # returns user's model object with that username
            user = user_repository.find_by_username(request.form["username"].lower())

        except:
            # fixme
            return render_template(
                "./auth/login_view.html",
                title=title,
                is_error=True,
                error_msg="Bir xəta baş verdi!" " Zəhmət olmasa yenidən cəhd edin.",
                form=login_form,
            )

        # create an object for user_controller to check password
        user_controller = UserController(user, user_repository)

        if user_controller.validate_username_and_password(
            request.form["password"], request.form["username"].lower()
        ):
            if keywords_model := keyword_repo.get_current_keyword():
                model = keywords_model[0]

                print(
                    "I AM INSIDE (keywords_model := keyword_repo.get_current_keyword())"
                )
                print("SETTING USER SESSIONS AND KEYWORD")
                user_controller.set_session(
                    "keyword", {"week_no": model.week_no, "key": model.keyword}
                )

            if request.args.get("next"):
                return redirect(str(request.args.get("next")))

            if not session["is_admin"]:
                return redirect("/")

            else:
                # if 1 in session['all_user_roles']:
                #
                #     return redirect('/admin/all')

                return redirect("/admin/")

        # Zəhmət olmasa login və ya şifrənizi düzgün daxil edin!
        return render_template(
            "./auth/login_view.html",
            title=title,
            is_error=True,
            error_msg="Zəhmət olmasa login və ya şifrənizi düzgün daxil edin!"
            "və ya HƏFTƏ İÇİ daxil olmaqa çalışın.",
            form=login_form,
        )

    if not current_user.is_authenticated:
        return render_template("./auth/login_view.html", title=title, form=login_form)
    else:
        return redirect("/")
