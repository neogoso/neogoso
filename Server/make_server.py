# -*- coding: utf-8 -*-

import app.core as core

server = core.Init()
app = server.app

from app.view import *

if __name__ == '__main__':
	app.run(host = '0.0.0.0',port = 8080, debug = True)