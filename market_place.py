import sqlalchemy
import flask
import sys
from flask import Flask, request
from bd_info import User, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import requests

app = Flask(__name__)
engine = create_engine(f'sqlite:///nodes.sqlite3')
Base.metadata.bind = engine
_factory = sessionmaker(bind=engine)
#
database_loaded = False


@app.route('/v1/get/<int:uid>', methods=['GET'])
def new_wallet(uid):
    global database_loaded
    session = _factory()
    user = session.query(User).filter(User.id == uid).first()
    if not user:
        return flask.jsonify({'error': 'User not found'})
    print(flask.jsonify(user.to_dict()))
    return flask.jsonify(user.to_dict())


@app.route('/v1/register', methods=['POST'])
def registration():
    global database_loaded
    session = _factory()
    if not request.json:
        return flask.jsonify({'error': 'Empty request'})
    url = 'http://mabaker.pythonanywhere.com/blockchainapi/v1/new_wallet'
    repos = requests.get(url + '/new_wallet').json()
    user = User(role=request.json['role'], name=request.json['name'], login=request.json['login'], password=request.json['password'],
                surname=request.json['surname'], public_key=repos['publicKey'], private_key=repos['privateKey'], lvl=1)
    session.add(user)
    session.commit()
    return flask.jsonify({'success': 'OK'})


@app.route('/v1/delete/<int:uid>', methods=['POST'])
def delete(uid):
    session = _factory()
    if not request.json:
        return flask.jsonify({'error': 'Empty request'})
    user_to_delete = session.query(User).filter(User.id == uid).first()
    session.delete(user_to_delete)
    session.commit()
    return flask.jsonify({'success': 'OK'})


@app.route('/v1/edit_info/<int:uid>', methods=['POST', 'GET', 'DELETE'])
def edit_info(uid):
    global database_loaded
    session = _factory()
    if not request.json:
        return flask.jsonify({'error': 'Empty request'})
    user = session.query(User).filter(id=uid).first()
    if not user:
        return flask.jsonify({'error': 'User not found'})
    user.role = request.json['role']
    user.name = request.json['name']
    user.login = request.json['login']
    user.avatar_url = request.json['avatar_url']
    user.password = request.json['password']
    user.surname = request.json['surname']
    user.team_id = request.json['team_id']
    user.lvl = request.json['lvl']
    session.commit()
    user = session.query(User).filter(id=uid).first()
    return flask.jsonify(user.to_dict())


@app.route('/v1/login', methods=['GET', 'POST'])
def login():
    global database_loaded
    session = _factory()
    if not request.json:
        return flask.jsonify({'error': 'Empty request'})
    user = session.query(User).filter(User.login == request.json['login']).first()
    if not user:
        return flask.jsonify(-1)
    if user.password == request.json['password']:
        return flask.jsonify(user.id)
    else:
        return flask.jsonify(-1)


if __name__ == '__main__':
    app.run(debug=True)
