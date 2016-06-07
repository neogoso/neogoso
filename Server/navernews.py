# -*- coding: utf-8 -*-

import app.core as core

server = core.Init()
db = server.db

from model import *

import sys
import urllib, urllib2
import datetime
import time
import json

import requests # ranking
from BeautifulSoup import BeautifulSoup, NavigableString # memo

class NaverNewsCrawler(object):
    def __init__(self):
        pass

    def get_articles(self, 
                     date = (sys.argv[1],
                             sys.argv[2])):
        _headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; ko-KR))',
            'Host' : 'entertain.naver.com'
        }

        startdate = datetime.date(
            *map(int, date[0].split('-')))

        enddate = datetime.date(
            *map(int, date[1].split('-')))

        list_articles = []


        print 'Extracting articles [ranking...]'

        t = startdate
        
        # ranking
        while t < enddate:

            date_curr = '%s-%s-%s'\
                    % (str(t.year),
                       ('0'+str(t.month))[-2:],
                       ('0'+str(t.day))[-2:])
            response = requests.get(
                'http://entertain.naver.com/ranking/page.json?&type=default&date=%s' % date_curr,
                headers = _headers
            )

            jsondata = json.loads(response.text)

            for d in jsondata['articles']:
                title = d['contentsArticle']['title']
                oid = d['contentsArticle']['office']['id']
                aid = d['contentsArticle']['articleId']
                
                if not (not oid or not aid) : 
                    list_articles.append({
                        'title' : title, 'oid' : oid,
                        'aid' : aid
                    })
            t += datetime.timedelta(days = 1)

        print 'Extracting articles [memo...]'
        
        t = startdate

        # memo
        #for i in xrange(5):
	    #z = datetime.datetime.now() - datetime.timedelta(7 * i)
        while t < enddate:
            date_curr = "%s%s%s" % (
                str(t.year),
                ('0'+str(t.month))[-2:],
                ('0'+str(t.day))[-2:])


            response = requests.get(
                'http://entertain.naver.com/ranking/memo?date=%s' % date_curr,
                headers = _headers
            )

            soup = BeautifulSoup(response.text)

            for article in soup.findAll(
                'li', attrs = {'class':''}):
                z = article.find(
                    'a', attrs = {'class':'tit'})
                id_raw = z['href'].split('?')[1].split('&')
                
                title = z.text
                oid = id_raw[0].split('=')[1]
                aid = id_raw[1].split('=')[1]
                
                if not (not oid or not aid) : 
                    list_articles.append({
                        'title' : title,
                        'oid' : oid, 'aid' : aid
                    })
            t += datetime.timedelta(days = 1)
        print 'Total : %d articles' % len(list_articles)

        return list_articles

    def get_comments(self, oid, aid):
        print 'Current article : oid %s, aid %s' % (oid, aid)

        pagesize = 20
        page = 0

        #while(pagesize * page < total):
        while True:
            page += 1

            urlform = '''https://apis.naver.com/commentBox/cbox5/web_naver_list_jsonp.json?
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

            url = urlform\
                    .replace('\n', '')\
                    .replace('\t', '')\
                    .replace(' ', '')

            url = url\
                    .replace(
                        'page=1',
                        'page=%d' % page)\
                    .replace(
                        'pageSize=20',
                        'pageSize=%d' % pagesize)\
                    .replace(
                        'objectId=news109' + '%2C' + '0003328307',
                        'objectId=news%s' % oid + '%2C' + '%s' % aid)
            

            request = urllib2.Request(url)
            request.add_header(
                'host', 'apis.naver.com')
            request.add_header(
                'referer',
                'http://entertain.naver.com/comment/list?oid=%s&aid=%s'\
                % (oid, aid))

            response = urllib2.urlopen(request)

            raw = response.read().replace('\\x', '\\u00')

            jsondata = json.loads(
                raw[10:-2].replace('"', "\"")) 

            list_comments = []
            
            try:
                jsondata['result']['commentList']
            except KeyError:
                'No comments'
                return []

            for c in jsondata['result']['commentList']:
                list_comments.append({
                    'commentNo' : c['commentNo'],
                    'contents' : c['contents'],
                    'maskedUserId' : c['maskedUserId'],
                    'modTime' : c['modTime'],
                    'objectId' : c['objectId'],
                    'parentCommentNo' : c['parentCommentNo'],
                    'profileUserId' : c['profileUserId'],
                    'regTime' : c['regTime'],
                    'userIdNo' : c['userIdNo'],
                    'userName' : c['userName']})

            return list_comments

    def get_replies(self,
                    parentCommentNo, oid, aid, page = 1):
        urlform = '''https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json?
        ticket=news&
        templateId=default_ent&
        pool=cbox5&
        _callback=&
        lang=ko&country=KR&
        objectId=news076%2C0002938677&
        categoryId=&
        pageSize=100&
        indexSize=10&
        groupId=&
        parentCommentNo=615919102&
        page=1&
        userType=&
        moreType=next'''\
                .replace('\n', '')\
                .replace('\t', '')\
                .replace(' ', '')

        url = urlform\
                .replace(
                    'objectId=news076%%2C0002938677',
                    'objectId=news%s' % oid + '%2C' + '%s' % aid)\
                .replace(
                    'parentCommentNo=615919102',
                    'parentCommentNo=%d'\
                    % parentCommentNo)\
                .replace(
                    'page=1',
                    'page=%d' % page)

        request = urllib2.Request(url)
        request.add_header(
            'host', 'apis.naver.com')
        request.add_header(
            'referer',
            'http://entertain.naver.com/ranking/comment/list?oid=%s&aid=%s'\
            % (str(oid), str(aid)))

        response = urllib2.urlopen(request)

        raw = response.read().replace(
            '\\x', '\\u00').replace('"', "\"")
        
        jsondata = json.loads(raw[10:-2])
        list_replies = []

        for c in jsondata['result']['commentList']:
            list_replies.append({
                'commentNo' : c['commentNo'],
                'contents' : c['contents'],
                'maskedUserId' : c['maskedUserId'],
                'modTime' : c['modTime'],
                'objectId' : c['objectId'],
                'parentCommentNo' : c['parentCommentNo'],
               # 'profileUserId' : c['profileUserId'],
                'regTime' : c['regTime'],
                #'userIdNo' : c['userIdNo'],
                'userName' : c['userName']})

        return list_replies

if __name__ == '__main__':
    nnc = NaverNewsCrawler()
    list_articles = nnc.get_articles()
    
    urlform = 'http://entertain.naver.com/read?oid=%s&aid=%s'

    for article in list_articles:
        title = article['title']
        oid = article['oid']
        aid = article['aid']

        # comments
        list_comments = nnc.get_comments(oid = oid, aid = aid)
        
        for comment in list_comments:
            comment['title'] = title
            comment['oid'] = oid
            comment['aid'] = aid
            comment['url'] = urlform % (oid, aid)

            dbcomment = NaverNews(
                comment['commentNo'],
                comment['contents'],
                comment['maskedUserId'],
                comment['modTime'],
                comment['objectId'],
                comment['parentCommentNo'],
                #comment['profileUserId'],
                comment['regTime'],
               # comment['userIdNo'],
                comment['userName'],
                comment['title'],
                comment['oid'],
                comment['aid'],
                comment['url'] 
                )
            try :
                db.session.add(dbcomment)
                db.session.commit()
            except Exception : 
                db.session.rollback()


        # replies (= comment of comments)
        for comment in list_comments:
            list_replies = nnc.get_replies(
                parentCommentNo = comment['parentCommentNo'],
                oid = oid, aid = aid)

            for e in list_replies:
                comment = e
                comment['title'] = title
                comment['oid'] = oid
                comment['aid'] = aid
                comment['url'] = urlform % (oid, aid)
                dbcomment = NaverNews(
                    comment['commentNo'],
                    comment['contents'],
                    comment['maskedUserId'],
                    comment['modTime'],
                    comment['objectId'],
                    comment['parentCommentNo'],
                    #comment['profileUserId'],
                    comment['regTime'],
                    #comment['userIdNo'],
                    comment['userName'],
                    comment['title'],
                    comment['oid'],
                    comment['aid'],
                    comment['url'] 
                    )
                try :
                    db.session.add(dbcomment)
                    db.session.commit()
                except Exception : 
                    db.session.rollback()

