from flask import Blueprint, render_template

bp = Blueprint("Services", __name__)

@bp.route('/Services')
def services():
    return render_template('home/Services.html')