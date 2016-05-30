#-*- coding: utf-8 -*-
import urllib
import urllib2

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

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

request = urllib2.Request(url)
request.add_header('host','apis.naver.com')
request.add_header('referer','http://entertain.naver.com/comment/list?oid=109&aid=0003328307&gid=999339&cid=1017324')
response = urllib2.urlopen(request)


result = response.read()
result = result[10:-2];

import json
json_acceptable_string = result.replace("'", "\"")
d = json.loads(json_acceptable_string)
print d['result']['count']
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
for comment in d['result']['commentList'] :
	row = ''
	for attribute in column :
		row += str(comment[attribute]) + " "
	print row
