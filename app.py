#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask_socketio import SocketIO,send
from unqlite import UnQLite
import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@socketio.on('message')
def handle_message(message):
    print ('message : ' + message)
    send(message, broadcast = True)
    #emit('handle_forward_message', data, broadcast=True)

@socketio.on('connect')
def handle_connect():
    print 'socket conectado'

@socketio.on('disconnect')
def on_leave():
	print 'Usuario desconectado'

@socketio.on('handle_forward_message')
def handle_forward_message(message):
    print('received message: ' + message)
    #emit('my response', data, broadcast=True)

def connection():
	return UnQLite('db/socket.db')

def drop_collections():
	db = connection()
	if db.collection('usuarios').exists() == True:
		db.delete('usuarios')

def cargar_usuarios():
	url = 'http://localhost:5001/usuario/listar_usuarios'
	response = json.loads(requests.get(url).text)
	db = connection()

	if db.collection('usuarios').exists() != True:
		db.collection('usuarios').create()

	for usuario in response:
		db.collection('usuarios').store(usuario)

def query():
	db = connection()
	print db.collection('usuarios').all()

if __name__ == '__main__':
	#socketio.run(app, port=4000)
	#drop_collections()
	#cargar_usuarios()
	