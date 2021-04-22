from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

import sqlalchemy


class Book(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'books'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    author = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    annotation = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    genre_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("genres.id"))
    created_date = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    img_file = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    text_file = sqlalchemy.Column(sqlalchemy.String)

    genre = orm.relation('Genre')
