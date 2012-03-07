#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# this script serves to model a tweet
#
# @author Yuan JIN
# @contact chengdujin@gmail.com
# @since 2012.03.07
# @latest 2012.03.07
#

# reload the script encoding
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

class Tweet:
    'class dedicated to tweet modeling'
    def __init__(self, id_ = None, text= None, favorited = None, created_at= None, retweeted = None, source = None):
        self.id_ = id_
        self.text = text
        self.favorited = favorited
        self.created_at = created_at
        self.retweeted = retweeted
        self.source = source

        # properties importantes
        self.users = []
        self.urls = []
        self.hashtags = []

        self.keywords = []
        self.chinese = []
        self.latin = []

    def __str__(self):
        return 'keywords:\n' + str(self.keywords) + '\nchiense:\n' + str(self.chinese) + '\nlatin:\n' + str(self.latin) + '\nurls:\n' + str(self.urls) + '\nhashtags:\n' + str(self.hashtags) + '\nusers:\n' + str(self.users) + '\ncreated_at:\n' + str(self.created_at) + '\nsource:\n' + str(self.source) + '\n'

    def 
