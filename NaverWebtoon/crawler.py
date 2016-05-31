#-*- coding: utf-8 -*-
import urllib
import urllib2

import sys
import re
import json, cjson, jsonlib

reload(sys)
sys.setdefaultencoding('utf-8')

titleId = '663887'
no = '64'

url1 = 'http://comic.naver.com/ncomment/ncomment.nhn?titleId=' + titleId + '&no='+ no + '&levelName=WEBTOON#'
#http://comic.naver.com/ncomment/ncomment.nhn?titleId=663887&no=각화 number&levelName=WEBTOON##
request = urllib2.Request(url1)
response = urllib2.urlopen(request)


for line in response.read().splitlines() :
	if 'lkey' in line :
		lkey = line.split("'")[1]
	if 'pageSize' in line :
		number = [int(s) for s in line.split() if s.isdigit()]
		page_size = number[0]

print lkey
print page_size


for page_no in range(1, 460):
	url = 'http://comic.naver.com/comments/list_comment.nhn'
	data = {'ticket':'comic1',
			'object_id':titleId + '_' + no,
			'lkey':lkey,
			'page_size':page_size,
			'page_no':page_no,
			'sort':'newest'}
	data = urllib.urlencode(data)
	request = urllib2.Request(url, data)
	request.add_header('Connection','keep-alive')
	request.add_header('Content-Type','application/x-www-form-urlencoded; charset=UTF-8')
	request.add_header('Referer',url1)
	response = urllib2.urlopen(request)

	json_acceptable_string = response.read().replace("'", "\"").replace('\\x', '\\u00') 
	d = json.loads(json_acceptable_string)

	# comment_list가 size가 0일때까지 page_no를 증가시키면 될듯
	for comment in d['comment_list']:
		print comment['registered_ymdt'] + " " + \
		comment['enc_writer_id'] + " " + \
		comment['writer_nickname'] + " " + \
		comment['modified_ymdt'] + " " + \
		comment['object_id'] + " " + \
		comment['writer_id'] + " " + \
		comment['contents'] + " " + \
		str(comment['comment_no'])
