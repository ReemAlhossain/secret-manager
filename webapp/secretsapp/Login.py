from flask import Blueprint, render_template

bp = Blueprint("Login", __name__)

@bp.route('/login')
def registration():
    return render_template('home/index.html')






