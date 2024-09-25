from flask import Blueprint, render_template

bp = Blueprint("Registration", __name__)

@bp.route('/Registration')
def registration():
    return render_template('home/Registration.html')