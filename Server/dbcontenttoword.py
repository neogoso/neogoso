#-*- coding: utf-8 -*-

import app.core as core

server = core.Init()
db = server.db


from model import *


from konlpy.tag import Twitter
import time

start = 1
term = 100

wordtypes = ['Noun','Verb','Adjective','KoreanParticle']

words = {}
for atype in wordtypes :
	words[atype] = []

t = time.time()

while True : 
	comments = NaverWebtoon.query.with_entities(NaverWebtoon.contents).slice(start,start+term).all();
	start += term

	if not comments :
		break
	twit = Twitter()

	for comment in comments :
		results = twit.pos(comment[0])
		for result in results :
			(word, wordtype) = result
			if wordtype in wordtypes :
				words[wordtype].append(word)

t2 = time.time()


for wordtype in wordtypes :
	print wordtype
	words[wordtype] = list(set(words[wordtype]))
	results = words[wordtype]
	for result in results :
		print result,

for wordtype in wordtypes :
	print wordtype + ":" + str(len(words[wordtype])) 

print "time" + ":", t2 - t