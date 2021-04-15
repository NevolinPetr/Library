import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Genre(SqlAlchemyBase):
    __tablename__ = 'genres'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)

    book = orm.relation("Book", back_populates='genre')
