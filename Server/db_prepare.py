# -*- coding: utf-8 -*-

import app.core as core

server = core.Init()
db = server.db


from model import *

#db.drop_all()
#db.create_all()

db.create_all()
