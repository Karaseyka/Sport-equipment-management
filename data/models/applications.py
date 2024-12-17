import sqlalchemy
from flask_login import UserMixin

from sqlalchemy_serializer import SerializerMixin

from data.database.db_session import SqlAlchemyBase

# Заявки пользователей
class Applications(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'applications'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    description = sqlalchemy.Column(sqlalchemy.String)
    count = sqlalchemy.Column(sqlalchemy.Integer)
    user = sqlalchemy.Column(sqlalchemy.Integer)
    status = sqlalchemy.Column(sqlalchemy.String)