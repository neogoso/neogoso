# -*- coding: utf-8 -*-

import math
import json
import os
import tweepy

_path = os.path.abspath(__file__)
_dir_path = os.path.dirname(_path)

with open(os.path.join(_dir_path, 'appinfo.json')) as p:
    _appinfo = json.loads(p.read())

def print_unsafe(s):
    ''' Print s if UnicodeEncodeError is not raised
    * Just for debugging! Appropriate encoding detection
    is needed.
    '''
    try:
        print s
    except UnicodeEncodeError:
        print '(Can\'t be encoded!)'

class TwitterCrawler(object):
    ''' A Twitter crawler '''
    def __init__(self, 
                 appinfo = _appinfo,
                 wait_ratelimit = False,
                 *args, **kwargs):
        ''' Class initialization '''
        self.appinfo = appinfo
        self.wait_ratelimit = wait_ratelimit

    def authenticate(self):
        ''' Push the keys and tokens to OAuth to get the
        access to the API
        '''
        # set OAuth
        self.auth = tweepy.OAuthHandler(
            self.appinfo['consumer'],
            self.appinfo['consumer_secret'])

        self.auth.set_access_token(
            self.appinfo['token'],
            self.appinfo['token_secret'])

        # TODO : Encrypt the contents of appinfo.json

        # API access
        self.api = tweepy.API(
            self.auth,
            wait_on_rate_limit = self.wait_ratelimit
        ) # TODO : Bypass the rate limit of Twitter API
 
    def search(self, target, date, maxnum = 10):
        ''' Collect all the tweets with the keyword
        self.target, in the range self.date[0] -
        self.date[1]
        '''
        self.target = target
        self.date = date

        '''
        if maxnum <= rpp_max:
            _rpp = maxnum
        else:
            _rpp = rpp_max
        '''

        # TODO : Filter the items in the specific range of date

        cursor = tweepy.Cursor(
            self.api.search,
            q = self.target,
            result_type = 'recent',
            show_user = True)

        return cursor.items(maxnum)

def test():
    ''' Test routine : Seo Ji-Su in Lovelyz '''
    tc = TwitterCrawler()
    tc.authenticate()

    list_tweets = tc.search(
        target = '서지수',
        date = ((2015, 03, 01), (2016, 05, 30)),
        maxnum = 30)

    for index, tweet in enumerate(list_tweets):
        print '[%04dth result]' % (index+1)
        print '<Info>', tweet.created_at, '| <Content>',
        print_unsafe(tweet.text.replace('\n', '\\n'))
        print

if __name__ == '__main__':
    test()
