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
import re
from sqll import *

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sportequip.db"

db_session.global_init("data/instance/sportequip.db")

manager = LoginManager(app)
manager.init_app(app)
db_ses = db_session.create_session()


# пример запроса в БД
# db_ses.query(User).get(user_id)

# загрузка ползователя
@manager.user_loader
def load_user(user_id):
    return db_ses.query(User).get(user_id)


# Страница при входе на сайт
@app.route("/", methods=["GET"])
def welcome_page():
    return "типа самый важный"
    return "Для работы с сайтом требуется авторизация"


# Регистрация пост и гет методы
@app.route("/register/", methods=["POST"])
def register_post():
    PASSWORD_REGEXP = r'^[A-Za-z0-9!@#$%^&*()_+=-{}\[\]|;:\'",.<>?\\\/`~]{8,}$'
    LOGIN_REGEXP = r'^[A-Za-z0-9!@#$%^&*()_+=-{}\[\]|;:\'",.<>?\\\/`~]+$'

    params = request.json
    user_list = db_ses.query(User).all()
    user_logins = [i.name for i in user_list]
    if not (re.fullmatch(PASSWORD_REGEXP, params["password"]) and re.fullmatch(LOGIN_REGEXP, params["login"])):
        return "", 418

    if "is_admin" in params:
        if params["login"] in user_logins:
            return "", 401
        if params["is_admin"]:
            user = User(name=params["login"], password=generate_password_hash(params["password"]), type="admin")

        else:
            user = User(name=params["login"], password=generate_password_hash(params["password"]), type="user")
        db_ses.add(user)
        db_ses.commit()
        login_user(user)
        return "/profile/", 201
    else:
        user = db_ses.query(User).filter_by(name=params["login"]).first()
        print(user)
        if not user or not check_password_hash(user.password, params["password"]):
            return "", 401
        login_user(user)
        return "/profile/", 201


@app.route("/register/", methods=["GET"])
def register_get():
    return render_template('register.html')


@app.route("/profile/", methods=["GET"])
@login_required
def profile_get():
    cur_user = flask_login.current_user
    if cur_user.type == "user":
        items_of_inventory = db_ses.query(Inventory).filter_by(id=cur_user.id).all()
        return render_template('polzovatel.html', name=cur_user.name, inventory=items_of_inventory)
    else:

        items_of_inventory = db_ses.query(Inventory).filter_by(admin=cur_user.id).all()

        return render_template('admin.html', name=cur_user.name, inventory=items_of_inventory)

@app.route("/profile/", methods=["POST"])
@login_required
def profile_post():
    cur_user = flask_login.current_user
    if cur_user.type == "admin":
        name = request.form['name_item']
        quantity = request.form['quantity']
        condition = request.form['condition']
        db_ses.add(Inventory(name=name, count=quantity, state=condition, admin=cur_user.id))
        db_ses.commit()
        items_of_inventory = db_ses.query(Inventory).filter_by(admin=cur_user.id).all()
        return render_template('admin.html', name=cur_user.name, inventory=items_of_inventory)
    return render_template("polzovatel.html")



@app.route('/add_users/')
@login_required
def add_users():
    users = db_ses.query(User).filter_by(type="user", invent=None).all()
    return render_template('add_users.html', users=users)


@app.route('/add_user_to_inventory/', methods=['POST'])
@login_required
def add_user_to_inventory():
    user_id = request.json.get('id')
    goal_user = db_ses.query(User).filter_by(id=user_id).first()
    goal_user.invent = flask_login.current_user.id
    db_ses.add(goal_user)
    db_ses.commit()
    return "", 201


# -----------------


if __name__ == "__main__":
    app.run(debug=True)
