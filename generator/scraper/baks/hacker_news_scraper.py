#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# this script serves to grab the latest items in the hacker news
# stream, and store them into the mongodb
#
# @author Yuan JIN
# @contact chengdujin@gmail.com
# @since 2012.02.29
# @latest 2012.03.01

# reload the script encoding
import sys
reload(sys)
sys.setdefaultencoding("UTF-8")


def update_and_insert(db, doc):
    'dealing with mongodb'
    cursor = db.hn_articles.find({'title':'%s' % doc['title']})
    if cursor.count() > 0:
        for record in cursor:
            updated = False
            if record['postedago'] <> doc['postedago']:
                db.hn_articles.update(record, doc)
                updated = not updated
            elif record['commentcount'] <> doc['commentcount']:
            print doc
                db.hn_articles.update(record, doc)
                updated = not updated
            elif record['points'] <> doc['points']:
                db.hn_articles.update(record, doc)
                updated = not updated
            
            #if updated:
            #    print '* "%s" is updated!' % doc['title']
    else:
        #print '+ "%s" is added!' % doc['title']
        db.hn_articles.insert(doc) 

def parse_and_store(data):
    'parse the xml and store the result in mongodb'
    from pymongo import Connection
    con = Connection('localhost', 27017)
    db = con.hn_articles

    from BeautifulSoup import BeautifulStoneSoup
    root = BeautifulStoneSoup(data)
    page_items = root.contents[2].contents[1].contents
    for page_item in page_items:
        if page_item <> '\n':
            doc = {}
            for item in page_item.contents:
                if item <> '\n':
                    doc[item.name] = str(item.string)
            update_and_insert(db, doc)

def data_recv():
    'start a http get request'
    import httplib
    con = httplib.HTTPConnection('api.ihackernews.com')
    con.request("GET", "/page?format=xml")
    resp = con.getresponse()
    data = resp.read()
    con.close()
    return data

def main():
    'entrance to http get, parsing and storing'
    data = data_recv()
    parse_and_store(data)

if __name__ == '__main__':
    main()
