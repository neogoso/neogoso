# -*- coding: utf-8 -*-

import sys
import re
import json
import random
import time
import urllib, urllib2

_title_id = 663887
_sleep_range = [i*0.001 for i in xrange(1, 10+1)]

class NaverWebtoonCrawler(object):
    def __init__(self):
        pass

    def get_url(self, episode):
        url = {}

        # url for whole webtoon page
        url['whole'] = 'http://comic.naver.com'\
                '/webtoon/detail.nhn'\
                '?titleId=%d'\
                '&no=%d'\
                '&weekday=tue'\
                % (_title_id, episode)

        # url for comment part
        url['comment'] = 'http://comic.naver.com'\
                '/ncomment/ncomment.nhn'\
                '?titleId=%d'\
                '&no=%d'\
                '&levelName=WEBTOON#'\
                % (_title_id, episode)

        # url for extracting comments' data
        url['data'] = 'http://comic.naver.com'\
                '/comments/list_comment.nhn'

        return url

    def get_commentdata(self, episode):
        url = self.get_url(episode)
        
        # get lkey, pageSize
        request = urllib2.Request(url['comment'])
        response = urllib2.urlopen(request)

        data = response.read()

        for line in data.splitlines():
            if 'lkey' in line:
                lkey = line.split("'")[1]

            if 'pageSize' in line:
                page_size = int(filter(
                    str.isdigit,line.split())[0])
        
        # get the total number of comments
        form = {
            'ticket' : 'comic1',
            'object_id' : '%d_%d' % (
                _title_id, episode),
            'lkey' : lkey,
            'page_size' : page_size,
            'page_no' : 1, # we can use ANY page
            'sort' : 'newest'
        }

        request = urllib2.Request(
            url['data'], urllib.urlencode(form))
        request.add_header(
            'Connection', 'keep-alive')
        request.add_header(
            'Content-Type',
            'application/x-www-form-urlencoded; charset=UTF-8')
        request.add_header(
            'Referer', url['comment'])

        response = urllib2.urlopen(request)

        jsondata = json.loads(
            response.read().replace(
                "'", "\"").replace('\\x', '\\u00'))

        commentnum = jsondata['total_count']

        # now iterate through the pages until commentnum
        count = 0
        page_no = 1
        comment_list_total = []

        while 1:
            # set form
            print 'page_no : %d' % page_no
            form['page_no'] = page_no

            # sleep in random time
            print 'Sleeping...'

            if page_no % 3 == 0:
                time.sleep(
                    random.choice(_sleep_range))

            # get jsondata
            request = urllib2.Request(
                url['data'], urllib.urlencode(form))
            request.add_header(
                'Connection', 'keep-alive')
            request.add_header(
                'Content-Type',
                'application/x-www-form-urlencoded;'\
                'charset=UTF-8')
            request.add_header(
                'Referer', url['comment'])

            response = urllib2.urlopen(request)

            jsondata = json.loads(
                response.read().replace(
                    "'", "\"").replace('\\x', '\\u00'))

            # extract the comments
            comment_list = jsondata['comment_list']
            count += len(comment_list)
            comment_list_total += comment_list

            print 'current : %d comments' % count

            if count >= commentnum:
                break

            page_no += 1
        return comment_list_total

def test():
    nwc = NaverWebtoonCrawler()
    
    # ex) all comments in episode 15
    for i, comment in enumerate(
        nwc.get_commentdata(episode = 15)):
        print '[%04dth]' % i,
        print comment['registered_ymdt'] + " " + \
		comment['enc_writer_id'] + " " + \
		comment['writer_nickname'] + " " + \
		comment['modified_ymdt'] + " " + \
		comment['object_id'] + " " + \
		comment['writer_id'] + " " + \
		comment['contents'] + " " + \
		str(comment['comment_no'])

if __name__ == '__main__':
    result = []

    nwc = NaverWebtoonCrawler()
    
    for episode in xrange(51, 52):
        print 'Episode : %d...........' % episode

        for i, comment in enumerate(
            nwc.get_commentdata(episode)):
				print comment['comment_no'], comment['up_count'], comment['down_count']

				'''
				result.append(comment['registered_ymdt'] + " " + \
                    comment['enc_writer_id'] + " " + \
                    comment['writer_nickname'] + " " + \
                    comment['modified_ymdt'] + " " + \
                    comment['object_id'] + " " + \
                    comment['writer_id'] + " " + \
                    comment['contents'] + " " + \
                    str(comment['comment_no']))
				'''

    print 'done!'
