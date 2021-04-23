from . import db_session
from .books import Book
from flask import jsonify, request

import flask
import shutil

blueprint = flask.Blueprint(
    'book_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/book')
def get_book():
    db_sess = db_session.create_session()
    book = db_sess.query(Book).all()
    return jsonify(
        {
            'books':
                [item.to_dict(only=('title', 'author', 'genre.title', 'created_date'))
                 for item in book]
        }
    )


@blueprint.route('/api/book/<int:book_id>', methods=['GET'])
def get_one_book(book_id):
    db_sess = db_session.create_session()
    book = db_sess.query(Book).filter(Book.id == book_id).first()
    if not book:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'book': book.to_dict(only=(
                'title', 'author', 'annotation', 'genre.title', 'created_date'))
        }
    )


@blueprint.route('/api/book', methods=['POST'])
def create_book():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['title', 'author', 'annotation', 'genre_id',
                  'created_date', 'img_file', 'text_file']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    book = Book(
        title=request.json['title'],
        author=request.json['author'],
        annotation=request.json['annotation'],
        genre_id=request.json['genre_id'],
        created_date=request.json['created_date'],
        img_file=request.json['img_file'].split('/')[-1],
        text_file=request.json['text_file'].split('/')[-1]
    )
    shutil.copy(request.json['img_file'], f'static/img/{request.json["img_file"].split("/")[-1]}')
    shutil.copy(request.json['text_file'], f'static/text/{request.json["text_file"].split("/")[-1]}')
    db_sess.add(book)
    db_sess.commit()
    return jsonify({'success': 'ok'})


@blueprint.route('/api/book/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    db_sess = db_session.create_session()
    book = db_sess.query(Book).filter(Book.id == book_id).first()
    if not book:
        return jsonify({'error': 'Not found'})
    db_sess.delete(book)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/book/<int:book_id>', methods=['PUT'])
def edit_book(book_id):
    db_sess = db_session.create_session()
    book = db_sess.query(Book).get(book_id)
    if not book:
        return jsonify({'error': 'Not found'})
    elif not request.json:
        return jsonify({'error': 'Empty request'})
    book.title = request.json['title'] if 'title' in request.json else book.title
    book.author = request.json['author'] if 'author' in request.json else book.author
    book.annotation = request.json['annotation'] if 'annotation' in request.json else book.annotation
    book.genre_id = request.json['genre_id'] if 'genre_id' in request.json else book.genre_id
    book.created_date = (request.json['created_date'] if 'created_date' in request.json
                         else book.created_date)
    book.img_file = (request.json['img_file'].split('/')[-1] if 'img_file' in request.json
                     else book.img_file)
    book.text_file = (request.json['text_file'].split('/')[-1] if 'text_file' in request.json
                      else book.text_file)
    db_sess.commit()
    return jsonify({'success': 'OK'})
