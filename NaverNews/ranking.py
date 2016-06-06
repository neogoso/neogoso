# coding: utf-8
import requests
import datetime
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; ko-KR))',
}

startdate = datetime.date(2016, 3, 20)
enddate = datetime.date(2016, 6, 1)

t = startdate
while t < enddate:

	t += datetime.timedelta(days=1)
	date = "%s-%s-%s" % (str(t.year),
                      ('0'+str(t.month))[-2:], ('0'+str(t.day))[-2:])
	print date
	response = requests.get('http://entertain.naver.com/ranking/page.json?&type=default&date=%s' % date, headers=headers)
	data = json.loads(response.text)

	for i in data["articles"]:
		url = "http://entertain.naver.com/read?oid=%s&aid=%s" % (i["contentsArticle"]["office"]["id"], i["contentsArticle"]["articleId"])
		print url
		print i["contentsArticle"]["title"]
