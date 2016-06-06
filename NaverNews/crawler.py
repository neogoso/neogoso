#-*- coding: utf-8 -*-
import urllib
import urllib2
from konlpy.tag import Kkma, Twitter
from konlpy.utils import pprint
import time

import sys
reload(sys)
import json
import re

def getComment(oid, aid):

	sys.setdefaultencoding('utf-8')
	total = 1000000; # can be modified
	step = 20
	cnt = 39
	while(step * cnt < total):
		cnt += 1
		url = '''
			https://apis.naver.com/commentBox/cbox5/web_naver_list_jsonp.json?
			ticket=news&
			templateId=default_ent&
			_callback=&
			lang=ko&
			country=KR&
			objectId=news109%2C0003328307&
			pageSize=20&
			indexSize=10&
			page=1&
			initialize=true&
			useAltSort=true&
			replyPageSize=100&
			sort=new&
			'''

		url = url.replace('\n','').replace('\t','').replace(' ','')
		url = url.replace("page=1", "page=%s" % str(cnt))
		url = url.replace("pageSize=20", "pageSize=%s" % str(step))
		url = url.replace("objectId=news109,0003328307", "objectId=news%s,%s" % (oid, aid))
		

		request = urllib2.Request(url)
		request.add_header('host','apis.naver.com')
		request.add_header('referer','http://entertain.naver.com/comment/list?oid=%s&aid=%s' % (oid, aid))
		response = urllib2.urlopen(request)

		result = response.read().replace('\\x', '\\u00')
		result = result[10:-2];
		json_acceptable_string = result.replace('"', "\"")

		d = json.loads(json_acceptable_string)

		for i in d['result']['commentList']:
			print i['contents']
		total = d['result']['count']['comment']
	
		print d['result']['pageModel']
		

	column ='''commentNo
			contents
			maskedUserId
			modTime
			modTimeGmt
			objectId
			parentCommentNo
			profileUserId
			regTime
			regTimeGmt
			userIdNo
			userName'''.replace('\t','').replace(' ','').split('\n')

	print column
	return

if __name__ == '__main__':
	getComment('076', '0002938677')
	
'''
t = time.time()
twit = Twitter()

for comment in d['result']['commentList']:
	#row = ''
	#for attribute in column :
	#	row += str(comment[attribute]) + " "
	#comment['contents']
	twit.pos(comment['contents'])
	#print type(twit.pos(comment['contents']))
	

print time.time() - t

'''
