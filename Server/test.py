#-*- coding: utf-8 -*-

import app.core as core

server = core.Init()
db = server.db

from model import *

while True:
	dbcomment = NaverWebtoon("","","","","","","",1)
	try :
		db.session.add(dbcomment)
		db.session.commit()
	except Exception:
		db.session.rollback()
		print 'break'
		break