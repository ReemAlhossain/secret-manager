from flask import Blueprint, render_template

bp = Blueprint("Contact", __name__)

@bp.route('/Contact')
def contact():
    return render_template('home/Contact.html')

