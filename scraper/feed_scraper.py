#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# this script serves to fetch all of a provider's feeds (a limit 
# for the historical feeds would be 5000). and then the feeds are
# stored in mongodb
#
# @author Yuan JIN
# @contact chengudjin@gmail.com
# @since 2012.03.03
# @latest 2012.03.03

#relaod the script encoding
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')


# CONSTANTS
DB = '176.34.54.120:27017'
SOURCE_URL = 'http://content.businessvalue.com.cn/feed'
#SOURCE_URL = 'http://www.caijing.com.cn/rss/political.xml'
SOURCE_NAME = 'biz_value'.strip().lower()
LIMIT = 2000
GOOGLE_REQUEST_URL = 'http://www.google.com/reader/atom/feed/%s?n=%s'


# Google OAuth
SCOPE = "http://www.google.com/reader/api http://www.google.com/reader/atom"
REQUEST_OAUTH_TOKEN_URL = "https://www.google.com/accounts/OAuthGetRequestToken?scope=%s" % SCOPE
AUTHORIZE_URL = "https://www.google.com/accounts/OAuthAuthorizeToken"
ACCESS_TOKEN_URL = "https://www.google.com/accounts/OAuthGetAccessToken"

CLIENT_ID = "149442296180.apps.googleusercontent.com"
CLIENT_SECRET = "w9M59S7pdsRUoZLCrMuy1hG8"


def store_feeds(feeds, collection):
    'store the feeds in mongodb '
    from pymongo.errors import CollectionInvalid
    from pymongo.collection import Collection
    from pymongo.connection import Connection
    con = Connection(DB)
    from pymongo.database import Database
    db = Database(con, 'articles')

    col = None
    try:
        col = db.create_collection(collection)
    except CollectionInvalid as e:
        col = Collection(db, collection)

    for feed in feeds:
        if 'title' in feed:
            cursor = col.find({'title':'%s' % feed['title']})
            if cursor.count() > 0:
                continue
        elif 'source' in feed:
            cursor = col.find({'source':'%s' % feed['source']})
            if cursor.count() > 0:
                continue
        col.save(feed)

def parse_feeds(data, limit):
    'parse out necessary information'
    feeds = []
    
    from BeautifulSoup import BeautifulStoneSoup
    root = BeautifulStoneSoup(data)

    # every feed item starts from 7 + 2*step
    end = int(limit) * 2 - 1
    for item in xrange(7, 7 + end, 2):
        try:
            xml_feeds = root.contents[1].contents[item].contents
            feed = {}
            for xml_feed in xml_feeds:
                if xml_feed.name == 'entry':
                    info = xml_feed.contents
                    category = []
                    for id, entry in enumerate(info):
                        if entry.name == 'category':
                            if not entry['term'][:5] == 'user/':
                                category.append(entry['term'])
                        if (id + 1) == len(info):
                            feed['title'] = entry.contents[0].string
                            feed['published'] = entry.contents[1].string
                    feed['category'] = category
            try:
                xml_feeds = root.contents[1].contents[item + 1]
                feed['source'] = xml_feeds['href']
                feed['author'] = xml_feeds.contents[1].contents[0].string
            except Exception as e:
	             pass
            if feed:
                feeds.append(feed)
        except Exception as ex:
            pass
    return feeds
    

def create_oauth_client():
    'authorize with google reader - get the access token'
    import oauth2
    consumer = oauth2.Consumer(CLIENT_ID, CLIENT_SECRET)

    import os.path
    if not (os.path.exists('access_token') and os.path.exists('access_token_secret')):
        client = oauth2.Client(consumer)
        
        # request oauth token
        response, content = client.request(REQUEST_OAUTH_TOKEN_URL, 'GET')
        import urlparse
        request_token = dict(urlparse.parse_qsl(content))
    
        # authorization
        print "Open this link in a browser..:"
        print "%s?oauth_token=%s" % (AUTHORIZE_URL, request_token['oauth_token'])
        print
        print "Press ENTER when ready.."
        raw_input()
        
        # get access token
        token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
        client = oauth2.Client(consumer, token)
        
        response, content = client.request(ACCESS_TOKEN_URL, 'GET')
        access_token = dict(urlparse.parse_qsl(content))
        
        # record the token
        f = open ('access_token', 'w')
        f.write (access_token['oauth_token'])
        f.close ()
        oauth_token = access_token['oauth_token']
            
        f = open ('access_token_secret', 'w')
        f.write (access_token['oauth_token_secret'])
        f.close ()
        oauth_token_secret = access_token['oauth_token_secret']
    else:
        # read in the token and secret from local disk
        f = open('access_token', 'r')
        oauth_token = f.read()
        f.close()
            
        f = open ('access_token_secret', 'r')
        oauth_token_secret = f.read()
        f.close()
    
    token = oauth2.Token(oauth_token, oauth_token_secret)
    client = oauth2.Client(consumer, token)
    return client
    
def retrieve_data(url, limit):
    'read from google reader service'
    # request access token or find it locally
    client = create_oauth_client()

    # unlimited access to a provider's historical feeds
    # courtesy of google
    url = GOOGLE_REQUEST_URL % (url, limit)
    response, feeds = client.request(url, 'GET')
    return feeds

def main():
    'entrance to feeds retrieval and storing'
    data = retrieve_data(SOURCE_URL, LIMIT)
    feeds = parse_feeds(data, LIMIT)
    store_feeds(feeds, SOURCE_NAME)

if __name__ == '__main__':
    main()
