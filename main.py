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
from data.models.applications import Applications
from requests import get
import re
from sqll import *
import io
import csv

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sportequip.db"

db_session.global_init("data/instance/sportequip.db")

manager = LoginManager(app)
manager.init_app(app)
db_ses = db_session.create_session()


# пример запроса в БД
# db_ses.query(User).get(user_id)
def getApplicationsOfAdmin(adminId):
    applications = db_ses.query(Applications).join(Inventory, Applications.inventId == Inventory.id).filter(
        Inventory.admin == adminId).all()
    return applications

# загрузка ползователя
@manager.user_loader
def load_user(user_id):
    return db_ses.query(User).get(user_id)


# Страница при входе на сайт
@app.route("/", methods=["GET"])
def welcome_page():
    return render_template("starter.html")


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

@app.route('/delete-item-plan/', methods=['POST'])
@login_required
def delete_item_plan():
    item_id = request.json.get('id')
    item = db_ses.query(Procurements).get(item_id)
    print(type(item_id), item_id, item)
    db_ses.delete(item)
    db_ses.commit()
    return redirect("/profile")



@app.route('/update-item-plan/', methods=['POST'])
@login_required
def update_item_plan():
    data = request.json
    id = data['id']
    name = data['name']
    count = data['count']
    supplier = data['supplier']
    price = data['price']
    invent_item = db_ses.query(Procurements).get(id)
    if invent_item:
        invent_item.name = name
        invent_item.count = count
        invent_item.supplier = supplier
        invent_item.price = price
        db_ses.commit()

    return render_template('plan_admin.html')


@app.route("/get_report/", methods=["GET"])
@login_required
def get_report():
    file = io.StringIO()
    writer = csv.writer(file, delimiter=";")
    writer.writerow(['предмет', 'количество', 'пользователь', 'статус'])
    for i in getApplicationsOfAdmin(flask_login.current_user.id):
        writer.writerow([db_ses.query(Inventory).get(i.inventId).name, i.count, i.user, i.status])
    file.seek(0)
    mem = io.BytesIO()
    mem.write(file.getvalue().encode('Windows-1251'))
    mem.seek(0)
    return send_file(
        mem,
        as_attachment=True,
        download_name='залупень.csv'
    )


@app.route("/profile/", methods=["GET"])
@login_required
def profile_get():
    cur_user = flask_login.current_user
    if cur_user.type == "user":
        items_of_inventory = db_ses.query(Inventory).filter_by(admin=cur_user.invent).all()
        appid1 = db_ses.query(Applications).filter_by(user=cur_user.name).all()
        appid = []
        if len(appid1) > 0:
            appid = [''] * appid1[-1].inventId
            for i in appid1:
                print(i.inventId, i.status)
                appid[i.inventId - 1] = i.status
            print(appid, appid1[-1].inventId)
        return render_template('polzovatel.html', name=cur_user.name, appid=appid, inventory=items_of_inventory,
                               id=cur_user.id, appid1=appid1)
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


    else:
        name_item = request.form['ItemName']
        db_ses.add(Applications(user=cur_user.id, status='ожидает подтверждения', inventId=name_item))
        db_ses.commit()

    return redirect("/profile/")


@app.route("/new_procurement/", methods=["POST"])
@login_required
def new_procurement():
    sp = request.json
    cur_user = flask_login.current_user
    db_ses.add(
        Applications(user=cur_user.name, status='ожидает подтверждения', inventId=sp['id'], description=sp['opisanie'],
                     count=sp['quantity']))
    db_ses.commit()
    return "", 201


@app.route('/add_users/')
@login_required
def add_users():
    cur_user = flask_login.current_user
    if cur_user.type == "admin":
        users = db_ses.query(User).filter_by(type="user", invent=None).all()
        return render_template('add_users.html', users=users, name=cur_user.name)
    return "", 403


@app.route('/plan_admin/', methods=["GET"])
@login_required
def plan_admin_get():
    cur_user = flask_login.current_user
    if cur_user.type == "admin":
        inventory = db_ses.query(Procurements).filter_by(admin=cur_user.id).all()
        return render_template('plan_admin.html', name=cur_user.name, inventory=inventory)
    return "", 403


@app.route('/plan_admin/', methods=["POST"])
@login_required
def plan_admin_post():
    cur_user = flask_login.current_user
    name_item = request.form['name_item']
    quantity = request.form['quantity']
    supplier = request.form['supplier']
    price = request.form['price']
    db_ses.add(Procurements(name=name_item, count=quantity, supplier=supplier, price=price, admin=cur_user.id))
    db_ses.commit()

    return redirect('/plan_admin/')


@app.route('/list_admin/')
@login_required
def list_admin():
    cur_user = flask_login.current_user
    if cur_user.type == "admin":
        users = db_ses.query(User).filter_by(type="user", invent=cur_user.id).all()
        return render_template('list_admin.html', users=users)
    return "", 403


@app.route('/application_list/', methods=['GET'])
@login_required
def application_list_admin_get():
    cur_user = flask_login.current_user
    if cur_user.type == "admin":
        applications = db_ses.query(Applications).join(Inventory, Applications.inventId == Inventory.id).filter(Inventory.admin == cur_user.id).all()
        inventory = db_ses.query(Inventory).all()
        return render_template('application_list_admin.html', applications=applications, inventory=inventory)
    return "", 403


@app.route('/add_user_to_inventory/', methods=['POST'])
@login_required
def add_user_to_inventory():
    user_id = request.json.get('id')
    goal_user = db_ses.query(User).filter_by(id=user_id).first()
    goal_user.invent = flask_login.current_user.id
    db_ses.add(goal_user)
    db_ses.commit()
    return "", 201


@app.route('/delete-item/', methods=['POST'])
@login_required
def delete_item():
    item_id = request.json.get('id')
    item = db_ses.query(Inventory).get(item_id)
    print(type(item_id), item_id, item)
    db_ses.delete(item)
    db_ses.commit()
    return redirect ("/profile")

@app.route('/polzovatelskie_zzzayavki/', methods=['GET'])
@login_required
def polzovatelskie_zzzayavki_get():
    cur_user = flask_login.current_user
    applications = db_ses.query(Applications).filter_by(user=cur_user.name).all()
    print(applications)
    inventory = db_ses.query(Inventory).all()
    print(inventory)
    return render_template('polzovatelskie_zzzayavki.html', applications=applications, inventory=inventory, name=cur_user.name)


@app.route('/delete-user/', methods=['POST'])
@login_required
def delete_user():
    user_id = request.json.get('id')
    print(user_id)
    db_ses.query(User).filter_by(id=user_id).update({'invent': None})
    db_ses.commit()
    return redirect("/profile")


@app.route('/update-item/', methods=['POST'])
@login_required
def update_item():
    data = request.json
    item_id = data['id']
    name = data['name']
    count = data['count']
    state = data['state']
    invent_item = db_ses.query(Inventory).get(item_id)
    if invent_item:
        invent_item.name = name
        invent_item.count = count
        invent_item.state = state
        db_ses.commit()

    return render_template('admin.html')


@app.route('/delete-apply/', methods=['POST'])
@login_required
def delete_apply():
    zzzayavka_id = request.json.get('id')
    print(zzzayavka_id)
    db_ses.query(Applications).filter_by(id=zzzayavka_id).update({'status': 'отклонена'})
    db_ses.commit()
    return redirect("/application_list/")


@app.route('/accept-apply/', methods=['POST'])
@login_required
def accept_apply():
    zzzayavka_id = request.json.get('id')
    print(zzzayavka_id)
    db_ses.query(Applications).filter_by(id=zzzayavka_id).update({'status': 'одобрена'})
    db_ses.commit()
    return redirect("/application_list/")


@app.route("/выйти/", methods=["GET"])
@login_required
def выйти():
    session.clear()
    return redirect("/register/")

if __name__ == "__main__":
    app.run(debug=True)
