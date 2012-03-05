#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# this script serves to retrieve all the tweets of a user, and
# do some text mining based on the data
#
# @author Yuan JIN
# @contact chengdujin@gmail.com
# @since 2012.03.01
# @latest 2012.03.01

# reload the script encoding
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')


def parse_and_store(data):
    from pymongo import Connection
    con = Connection('176.34.54.120', 27017)
    db = con.tweets

    from BeautifulSoup import BeautifulStoneSoup
    root = BeautifulStoneSoup(data)
    tweets = root.contents[2].contents
    lowest_id = ''
    for tweet in tweets:
        if tweet <> '\n':
            doc = {}
            for item in tweet.contents:
                if item <> '\n':
		    try:
                        doc[item.name] = str(item.string)
		    except Exception as e:
			print item
			print tweet
            if doc:
		if 'id' in doc:	
                    db.tweets.save(doc)
                    lowest_id = doc['id']
    return lowest_id

def data_retv(user, max_id):
    import httplib
    con = httplib.HTTPConnection("api.twitter.com")
    con.request("GET", "/1/statuses/user_timeline.xml?contributor_details=0&trim_user=1&count=200&screen_name=%s&%s" % (user, max_id))
    reply = con.getresponse()
    data = reply.read()
    con.close()
    return data

def main():
    'entrance to tweets retrieval and analysis'
    max_id = ''
    while True:
        data = data_retv('chengdujin', max_id)
        max_id = parse_and_store(data)
        print max_id
        if not max_id:
            break
        else:
            max_id = 'max_id=' + str(int(max_id) - 1)

if __name__ == '__main__':
    main()
