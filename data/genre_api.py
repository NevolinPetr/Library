from . import db_session
from .genres import Genre
from flask import jsonify, request

import flask

blueprint = flask.Blueprint(
    'genre_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/genre')
def get_genre():
    db_sess = db_session.create_session()
    genre = db_sess.query(Genre).all()
    return jsonify(
        {
            'genres':
                [item.to_dict(only=('id', 'title'))
                 for item in genre]
        }
    )


@blueprint.route('/api/genre/<int:genre_id>', methods=['GET'])
def get_one_genre(genre_id):
    db_sess = db_session.create_session()
    genre = db_sess.query(Genre).get(genre_id)
    if not genre:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'genre': genre.to_dict(only=('id', 'title'))
        }
    )


@blueprint.route('/api/genre', methods=['POST'])
def create_genre():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ['title']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    if 'id' in request.json:
        if db_sess.query(Genre).get(request.json['id']):
            return jsonify({'error': 'Id already exists'})
    genre = Genre(
        title=request.json['title'],
    )
    db_sess.add(genre)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/genre/<int:genre_id>', methods=['DELETE'])
def delete_genre(genre_id):
    db_sess = db_session.create_session()
    genre = db_sess.query(Genre).get(genre_id)
    if not genre:
        return jsonify({'error': 'Not found'})
    db_sess.delete(genre)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/genre/<int:genre_id>', methods=['PUT'])
def edit_genre(genre_id):
    db_sess = db_session.create_session()
    genre = db_sess.query(Genre).get(genre_id)
    if not genre:
        return jsonify({'error': 'Not found'})
    elif not request.json:
        return jsonify({'error': 'Empty request'})
    genre.title = request.json['title'] if 'title' in request.json else genre.title
    return jsonify({'success': 'OK'})
