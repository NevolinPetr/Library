from . import db_session
from .users import User
from flask import jsonify, request

import flask

blueprint = flask.Blueprint(
    'user_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/user')
def get_user():
    db_sess = db_session.create_session()
    user = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'surname', 'name', 'email', 'created_date'))
                 for item in user]
        }
    )


@blueprint.route('/api/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'user': user.to_dict(only=('id', 'surname', 'name', 'email', 'created_date'))
        }
    )


@blueprint.route('/api/user', methods=['POST'])
def create_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['surname', 'name', 'email', 'hashed_password']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    if 'id' in request.json:
        if db_sess.query(User).get(request.json['id']):
            return jsonify({'error': 'Id already exists'})
    user = User(
        surname=request.json['surname'],
        name=request.json['name'],
        email=request.json['email'],
        hashed_password=request.json['hashed_password']
    )
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/user/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    elif not request.json:
        return jsonify({'error': 'Empty request'})
    user.surname = request.json['surname'] if 'surname' in request.json else user.surname
    user.name = request.json['name'] if 'name' in request.json else user.name
    user.email = request.json['email'] if 'email' in request.json else user.email
    user.hashed_password = (request.json['hashed_password'] if 'hashed_password' in request.json
                            else user.hashed_password)
    return jsonify({'success': 'OK'})
