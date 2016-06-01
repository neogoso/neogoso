# coding: utf-8
import requests
from BeautifulSoup import BeautifulSoup, NavigableString
import datetime


headers = {
    	'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; ko-KR))',
}

for i in range(5):
	z = datetime.datetime.now() - datetime.timedelta(7 * i)
	date = "%s%s%s" % (str(z.year), ('0'+str(z.month))[-2:], ('0'+str(z.day))[-2:])
	response = requests.get('http://entertain.naver.com/ranking/memo?date=%s' % date, headers=headers)
	html = response.text
	soup = BeautifulSoup(html)

	for article in soup.findAll('li', attrs={"class":""}):
		z = article.find('a', attrs={"class":"tit"})
		ref = "http://entertain.naver.com" + z["href"]
		name = z.text
		print ref + "\n" + name

