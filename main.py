import flask_login
from flask import Flask, render_template, redirect, send_file, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user
from flask import request
from data.database import db_session
from data.models.user import User
from data.models.applications import Applications
from data.models.inventory import Inventory
from data.models.procurments import Procurements
from requests import get

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sportequip.db"

db_session.global_init("data/instance/sportequip.db")

manager = LoginManager(app)
manager.init_app(app)
db_ses = db_session.create_session()


if __name__ == "__main__":
    app.run(debug=True)