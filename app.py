#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask_socketio import SocketIO,send
from unqlite import UnQLite
import db
import requests
import json 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Operaciones SocketIO

@socketio.on('message')
def handle_message(data):
    print ('message : ' + data)
    db = connection()
    db.collection('conversacion_test').store(data)

    send(data, broadcast = True)
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

# Operaciones con la base de datos UnQlite

def connection():
	return UnQLite('db/socket.db')

# Main

if __name__ == '__main__':
	socketio.run(app, port=4000)
	#drop_collections()
	#cargar_usuarios()
	