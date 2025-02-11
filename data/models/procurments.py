import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import ForeignKey

from sqlalchemy_serializer import SerializerMixin

from data.database.db_session import SqlAlchemyBase

# Заявки на закупку
class Procurements(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'procurements'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    admin = sqlalchemy.Column(sqlalchemy.Integer)
    name = sqlalchemy.Column(sqlalchemy.String)
    count = sqlalchemy.Column(sqlalchemy.Integer)
    price = sqlalchemy.Column(sqlalchemy.Integer)
    supplier = sqlalchemy.Column(sqlalchemy.String)
    status = sqlalchemy.Column(sqlalchemy.String)
