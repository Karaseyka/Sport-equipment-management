import sqlalchemy
from flask_login import UserMixin

from sqlalchemy_serializer import SerializerMixin

from data.database.db_session import SqlAlchemyBase

# Заявки на закупку
class Procurements(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'procurements'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    count = sqlalchemy.Column(sqlalchemy.Integer)
    status = sqlalchemy.Column(sqlalchemy.String)
