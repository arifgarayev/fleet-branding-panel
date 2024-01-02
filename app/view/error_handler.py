from flask import Blueprint, render_template, redirect, session

app = Blueprint("error", __name__)

@app.route('/error')
def error():

    return render_template('./error/weekday_upload_err.html',
                                           title="XƏTA", fleet_name=session['internal_company_name'],
                                           internal_company_balance_ref=session['internal_company_balance_ref'],
                                           keyword=session["keyword"])


@app.errorhandler(405)
def not_a_weekday(e):
    # note that we set the 404 status explicitly

    return render_template('./error/weekday_upload_err.html',
                           title="XƏTA", fleet_name=session['internal_company_name'],
                           internal_company_balance_ref=session['internal_company_balance_ref'],
                           keyword=session["keyword"]
                           )


@app.errorhandler(Exception)
def page_not_found(e):
    # note that we set the 404 status explicitly
    print(e)
    return redirect('/')
