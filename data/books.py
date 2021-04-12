import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Book(SqlAlchemyBase):
    __tablename__ = 'books'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    author = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    annotation = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    genre_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("genres.id"))
    created_date = sqlalchemy.Column(sqlalchemy.Date, nullable=True)
    img_file = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    text_file = sqlalchemy.Column(sqlalchemy.String)
    genre = orm.relation('Genre')
