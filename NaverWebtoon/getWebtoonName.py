import urllib2
import requests
import sys
from BeautifulSoup import BeautifulSoup

reload(sys)

sys.setdefaultencoding("utf-8")

titleID = '663887'
no = 51

for no in range(2, 71):
	url = 'http://comic.naver.com/webtoon/detail.nhn?titleId=663887&no=' + str(no)

	request = urllib2.Request(url)
	response = urllib2.urlopen(request)
	soup = BeautifulSoup(response)

	for i in soup.findAll("meta", attrs={"property": "og:title"}):
		print no, str(i).split("content=\"")[1].split(" />")[0].split(" ")[-1].split("(")[0]
