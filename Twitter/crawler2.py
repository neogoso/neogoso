# -*- coding: utf-8 -*-

# inspired by https://github.com/Jefferson-Henrique/GetOldTweets-python

# Unlike TwitterCrawler() in crawler.py, AdvTwitterCrawler() can find
# the old tweets, even if they were written a few years ago.

# XXX : VEEEEEERY SLOW than crawler.py...
#       ... we have to find the bottleneck first...

import urllib, urllib2
import json
import re
import datetime
import sys
import pyquery

_urlform = 'https://twitter.com/i/search/timeline?f=realtime&q=%s&src=typd&max_position=%s'
_cmdform = '%s since:%s until:%s'
_headform = {'User-Agent'\
             : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}

def print_unsafe(s):
    try:
        print s
    except UnicodeEncodeError:
        print '(Can\'t encode!)'

class Tweet(object):
    ''' Small object for handling tweet's info '''
    def __init__(self):
        self.id = None
        self.permalink = None
        self.username = None
        self.text = None
        self.date = None
        self.retweets = None
        self.hashtags = None
        # self.favorites = None
        # self.mentions = None
        # self.geo = None

class AdvTwitterCrawler(object):
    ''' Advanced Twitter Crawler '''
    def __init__(self):
        ''' Class initialization '''
        pass

    def search(self, target, date, maxnum = 10):
        ''' Search the tweets for the target in the specific range
        of date
        '''
        self.target = target
        self.date = date
        
        return self._get_tweets(maxnum)

    def _get_jsondata(self, cursor_refresh):
        ''' Give the command to Twitter search website
        and retrive the result in json format
        '''
        cmd = _cmdform % (
            self.target, self.date[0], self.date[1])

        url = _urlform % (
            urllib.quote(cmd), cursor_refresh)

        request = urllib2.Request(
            url, headers = _headform)

        # TODO : Exception handling when failing to
        # get response
        response = urllib2.urlopen(request)

        jsondata = json.loads(response.read())

        return jsondata

    def _get_tweets(self, count_max):
        ''' Find the tweets, at most count_max '''
        results = []

        cursor_refresh = ''
        count = 0

        while 1:
            jsondata = self._get_jsondata(cursor_refresh)

            if len(jsondata['items_html'].strip()) == 0:
                break

            cursor_refresh = jsondata['min_position']
            list_tweetdata = pyquery.PyQuery(
                jsondata['items_html'])(
                    'div.js-stream-tweet')

            if len(list_tweetdata) == 0:
                break

            for tweetdata in list_tweetdata:
                query = pyquery.PyQuery(tweetdata)
                tweet = Tweet()

                # username
                tweet.username = query(
                    'span.username.js-action-profile-name b').text()

                # date
                datestr = int(query(
                    'small.time span.js-short-timestamp').attr(
                        'data-time'))

                tweet.date = datetime.datetime.fromtimestamp(datestr)

                # id
                tweet.id = query.attr('data-tweet-id')

                # permalink
                tweet.permalink = query.attr('data-permalink-path')

                # text
		tweet.text = re.sub(
                    r'\s+', ' ', 
                    query("p.js-tweet-text").text()\
                    .replace('# ', '#').replace('@ ', '@'))

                # retweets
                tweet.retweets = int(query(
                    'span.ProfileTweet-action--retweet '\
                    'span.ProfileTweet-actionCount').attr(
                        'data-tweet-stat-count').replace(',', ''))

                # hashtags
                tweet.hashtags = ' '.join(re.compile(
                    '(@\\w*)').findall(tweet.text))

                # stack the tweet
                results.append(tweet)
                count += 1

                print 'Status : Got %dth tweet...' % count

                if count >= count_max:
                    #break
                    return results

        #return results

def test():
    ''' Test routine '''
    tc = AdvTwitterCrawler()

    list_tweets = tc.search(
        target = '서지수',
        date = ('2015-05-01', '2015-05-10'),
        maxnum = 100)

    print '[Test for the target %s within the date %s - %s]'\
            % ('서지수', '2015-05-01', '2015-05-10')
    print '(Maximum number of tweets : %d)' % 100

    for index, tweet in enumerate(list_tweets):
        print '[%05dth]' % (index+1)
        print tweet.username, '|',
        print tweet.date, '|',
        print_unsafe(tweet.text)

if __name__ == '__main__':
    test()
