#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unqlite import UnQLite
import requests
import json
import pprint

def connection():
	return UnQLite('db/socket.db')

def create_collections():
	db = connection()
	if db.collection('usuarios').exists() == False:
		db.collection('usuarios').create()
	if db.collection('conversacion_test').exists() == False:
		db.collection('conversacion_test').create()

def drop_collections():
	db = connection()
	if db.collection('usuarios').exists() == True:
		db.delete('usuarios')
	if db.collection('conversacion_test').exists() == True:
		db.delete('conversacion_test')

def cargar_usuarios():
	url = 'http://localhost:5001/usuario/listar_usuarios'
	response = json.loads(requests.get(url).text)
	db = connection()

	if db.collection('usuarios').exists() != True:
		db.collection('usuarios').create()

	for usuario in response:
		db.collection('usuarios').store(usuario)

def filter_test(document):
	document = json.loads(document)
	return document['mensaje'] == 'porque?' and document['usuario'] == 'pepe'

def select_conversacion_test():
	db = connection()
	#rs = db.collection('conversacion_test').all()
	rs = db.collection('conversacion_test').filter(filter_test)
	for r in rs:
		print r

def query():
	db = connection()
	print db.collection('usuarios').all()

# Main

if __name__ == '__main__':
	#create_collections()
	#drop_collections()
	#cargar_usuarios()
	select_conversacion_test()
	