import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import ForeignKey

from sqlalchemy_serializer import SerializerMixin

from data.database.db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'user'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    type = sqlalchemy.Column(sqlalchemy.String)
    password = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    invent = sqlalchemy.Column(sqlalchemy.Integer)

