#-*- coding: utf-8 -*-

import app.core as core

server = core.Init()
db = server.db

from model import *

dbcomment = NaverWebtoon("","","","","","","","","","")