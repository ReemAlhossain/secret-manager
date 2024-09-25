import secrets

from flask import Flask

import secretsapp.home
import secretsapp.About
import secretsapp.Services
import secretsapp.Contact
import secretsapp.db as db
import secretsapp.Registration
import secretsapp.Login
import secretsapp.MySecrets


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = secrets.token_hex(64)

    app.teardown_appcontext(db.teardown_db)

    # Registering the 'home' Blueprint
    app.register_blueprint(secretsapp.home.bp)
    app.register_blueprint(secretsapp.About.bp)
    app.register_blueprint(secretsapp.Contact.bp)
    app.register_blueprint(secretsapp.Services.bp)
    app.register_blueprint(secretsapp.Registration.bp)
    app.register_blueprint(secretsapp.Login.bp)
    app.register_blueprint(secretsapp.MySecrets.bp)




    # Return the configured Flask application
    return app

