from flask import Blueprint, render_template

bp = Blueprint("MySecrets", __name__)

# Defining a route at '/MySecrets'
@bp.route('/MySecrets')
def my_secrets():
    return render_template('home/MySecrets.html')
