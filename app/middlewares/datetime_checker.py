import functools
from datetime import datetime

import pytz
from flask import Flask, request, Blueprint, session, make_response, redirect, render_template

app = Blueprint("middleware", __name__)

@app.before_request
def is_weekday():

    if request.method == 'POST':

        if not timezone_checker(session['is_admin']):

            return make_response("Not a weekday", 405)



def timezone_checker(is_admin):

    baku_timezone_now = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Baku'))

    if not is_admin and baku_timezone_now.weekday() > 4:

        return False

    return True



def date(req):


    def decorator(fn):

        @functools.wraps(fn)
        def wrapper(*args,
                    **kwargs):

            if req.method == "POST":

                if not timezone_checker(session['is_admin']):

                    return render_template('./error/weekday_upload_err.html',
                                           title="XƏTA", fleet_name=session['internal_company_name'],
                                           internal_company_balance_ref=session['internal_company_balance_ref']
                                           ), 405


            return fn(*args,
                      **kwargs)


        wrapper.__name__ = f"{fn.__name__}"
        wrapper.__module__ = fn.__module__

        return wrapper

    return decorator