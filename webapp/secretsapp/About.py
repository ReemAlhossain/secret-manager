from flask import Blueprint, render_template

bp = Blueprint("About", __name__)

@bp.route('/About')
def about():
    return render_template('home/About.html')






