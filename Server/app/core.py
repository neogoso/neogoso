# -*- coding: utf-8 -*-

server = None

def Init():
	from flask import Flask
	app = Flask(__name__)
	#import os
	#app.config.from_object('app.config.DefaultConfig')
	app.secret_key = '9a6f5a1119022ef417bdba70848aecb2be3af045185d13632dacd08d48f89ff7fa9fa8dca29577f93fb7d45ba4b3f339'
	app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:hacker@127.0.0.1/Comments?charset=utf8mb4'
	app.config['static_url_path'] = '/home/neogoso/Server/app/static'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.config['BCRYPT_LEVEL'] = 63

	from flask_sqlalchemy import SQLAlchemy
	db = SQLAlchemy(app)

	class MakeServerObject(object): pass
	global server
	server = MakeServerObject()
	server.app = app
	server.db = db
	#server.config = app.config
	return server