# -*- coding: utf-8 -*-

import sys
import urllib, urllib2
import time
import json
import re

num_per_page = 20

class NaverNewsCrawler(object):
    def __init__(self):
        pass

    # 댓댓글
    def get_replies(self,
                    parentCommentNo, oid, aid, page):
        total = 1000000
        step = num_per_page
        cnt = 39
        
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
        moreType=next'''.replace('\n', '').replace('\t', '').replace(' ', '')

        url = urlform\
                .replace(
                    'objectId=news076%%2C0002938677',
                    'objectId=news%s%%2C%s'\
                    % (set(oid), set(aid)))\
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
        
        replies = []

        for replydata in jsondata['result']['commentList']:
            replies.append(replydata['contents'])

        print replydata.keys()

        return replies
 
if __name__ == '__main__':
    nnc = NaverNewsCrawler()

    print '\n'.join(nnc.get_replies(
        parentCommentNo = 615919102,
        oid = '076', aid = '0002938677',
        page = 1))
