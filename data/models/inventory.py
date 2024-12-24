import sqlalchemy
from flask_login import UserMixin

from sqlalchemy_serializer import SerializerMixin

from data.database.db_session import SqlAlchemyBase


# Содержание инвентаря
class Inventory(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'inventory'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    count = sqlalchemy.Column(sqlalchemy.Integer)
    state = sqlalchemy.Column(sqlalchemy.String)
    admin = sqlalchemy.Column(sqlalchemy.Integer)
