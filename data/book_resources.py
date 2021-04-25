from . import db_session
from .books import Book
from flask import jsonify
from flask_restful import abort, reqparse, Resource

import shutil

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('author', required=True)
parser.add_argument('annotation', required=True)
parser.add_argument('img_file', required=True)
parser.add_argument('text_file', required=True)
parser.add_argument('genre_id', required=True, type=int)
parser.add_argument('created_date', required=True, type=int)


def abort_if_book_not_found(book_id):
    session = db_session.create_session()
    book = session.query(Book).get(book_id)
    if not book:
        abort(404, message=f"Book {book_id} not found")


class BookResource(Resource):
    def get(self, book_id):
        abort_if_book_not_found(book_id)
        session = db_session.create_session()
        book = session.query(Book).get(book_id)
        return jsonify({'book': book.to_dict(
            only=('title', 'author', 'genre_id', 'created_date', 'img_file', 'text_file'))})

    def delete(self, book_id):
        abort_if_book_not_found(book_id)
        session = db_session.create_session()
        book = session.query(Book).get(book_id)
        session.delete(book)
        session.commit()
        return jsonify({'success': 'OK'})


class BookListResource(Resource):
    def get(self):
        session = db_session.create_session()
        book = session.query(Book).all()
        return jsonify({'books': [item.to_dict(
            only=('title', 'author', 'genre.title', 'created_date')) for item in book]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        book = Book(
            title=args['title'],
            author=args['author'],
            annotation=args['annotation'],
            genre_id=args['genre_id'],
            created_date=args['created_date'],
            img_file=args['img_file'].split('/')[-1],
            text_file=args['text_file'].split('/')[-1]
        )
        shutil.copy(args['img_file'], f'static/img/{args["img_file"].split("/")[-1]}')
        shutil.copy(args['img_file'], f'static/text/{args["text_file"].split("/")[-1]}')
        session.add(book)
        session.commit()
        return jsonify({'success': 'OK'})
