import sqlite3
import json


def add_user(type, password, name):
    con = sqlite3.connect('data/instance/sportequip.db')
    cur = con.cursor()
    cur.execute("""INSERT INTO user (type, password, name) 
                       VALUES (?, ?, ?)
                    """, (type, password, name,))
    con.commit()
    return True


def add_procurements(name, count, status):
    con = sqlite3.connect("data/instance/sportequip.db")
    cur = con.cursor()
    cur.execute("""INSERT INTO procurements (name, count, status)
                        VALUES (?, ?, ?)
                    """, (name, count, status,))
    con.commit()
    return True


def add_item(name, count, state, admin):
    con = sqlite3.connect("data/instance/sportequip.db")
    cur = con.cursor()
    cur.execute("""INSERT INTO inventory (name, count, state, admin)
                        VALUES (?, ?, ?, ?)
                    """, (name, count, state, admin,))
    con.commit()
    return True


def delete_item(name):
    con = sqlite3.connect("data/instance/sportequip.db")
    cur = con.cursor()
    cur.execute("""DELETE FROM inventory WHERE name=?
                                                    """, (name,))
    con.commit()
    return True


def delete_user(name):
    con = sqlite3.connect("data/instance/sportequip.db")
    cur = con.cursor()
    cur.execute("""DELETE FROM user WHERE name=?
                                                    """, (name,))
    con.commit()
    return True


def update_item(name, new_count):
    con = sqlite3.connect("data/instance/sportequip.db")
    cur = con.cursor()
    cur.execute("""UPDATE inventory SET count=? WHERE name=?
                                                            """, (new_count, name,))
    con.commit()
    return True


def update_user(name, new_password):
    con = sqlite3.connect("data/instance/sportequip.db")
    cur = con.cursor()
    cur.execute("""UPDATE user SET password=? WHERE name=?
                                                        """, (new_password, name))
    con.commit()
    return True