#!/usr/bin/python
# -*- coding: utf-8 -*

##
# this script serves to monitor the registered user twitter account, 
# and publish certain tweets back to the project blog
#
# @author Yuan JIN
# @contact chengdujin@gmail.com
# @since 2012.03.02
# @latest 2012.03.02


def publish_candidates(user, candidates):
    'work with wordpress xml-rpc apis'
    'courtesy of jsnsipke from www.jansipke.nl/using-python-to-add-new-posts-in-wordpress'
    import datetime, time, xmlrpclib
    wp_url = 'http://176.34.54.120/blog/xmlrpc.php'
    wp_user = 'chengdujin'
    wp_password = 'sacrifice'
    wp_blogid = ''
    status_draft = 0
    status_published = 1
    server = xmlrpclib.ServerProxy(wp_url)
    
    content = ''
    for counter, cand in enumerate(candidates):
        created_at = cand['created_at']
        orthodoxized_time = orthodoxize_time(created_at, "%Y-%m-%d %H:%M:%S")
        content += '%s.[%s] %s\n%s\n\n' % (str(counter+1), orthodoxized_time, 'twitter.com/#/%s/status/%s' % (user, cand['id']), cand['text'])
    
    if content:
        title = time.strftime("%Y年%m月%d日", time.localtime()) + "Twitter上关于#socrates的言论总结"
        date_created = time.strftime("%Y%m%dT%H:%M:%SZ", time.gmtime())
        tags = ["twitter"]
        data = {'title':title, "description":content, "dateCreated":date_created, 'mt_keywords':tags}
        
        # publishing
        try:
            server.metaWeblog.newPost(wp_blogid, wp_user, wp_password, data, status_published)
        except Exception as e:
            print e
    
def orthodoxize_time(time_piece, time_format):
    'convert twitter time format to standard time format and Hong Kong time zone'
    import time
    # twitter time format to python time format
    orthodoxized_time = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(time_piece,'%a %b %d %H:%M:%S +0000 %Y'))
    
    # time zone conversion
    import pytz, datetime
    local = pytz.timezone ("Asia/Hong_Kong")
    naive = datetime.datetime.strptime (orthodoxized_time, "%Y-%m-%d %H:%M:%S")
    utc_time = naive.replace(tzinfo = pytz.utc)
    local_time = utc_time.astimezone (local)
    orthodoxized_time = local_time.strftime (time_format)
    
    return orthodoxized_time

def analyze_tweets(tweets):
    'keep what is necessary'
    first_candidates = []
    import twokenize
    for tweet in tweets:
        text = tweet['text']
        word_list = twokenize.tokenize(text)
        if '#socrates' in word_list:
            first_candidates.append(tweet)
    
    # filter out tweet not published today.
    import datetime
    second_candidates = []
    for first_cand in first_candidates:
        created_at = first_cand['created_at']
        orthodoxized_time = orthodoxize_time(created_at, "%Y%m%d")
        today = datetime.date.today().strftime("%Y%m%d")
        if orthodoxized_time == today:
            second_candidates.append(first_cand)
    
    return second_candidates

def parse_and_store(data):
    'parse out text and post-time of the tweets'
    from BeautifulSoup import BeautifulStoneSoup
    root = BeautifulStoneSoup(data)
    xml_tweets = root.contents[2].contents
    tweets = []
    for xml_tweet in xml_tweets:
        if xml_tweet <> '\n':
            tweet = {}
            for item in xml_tweet.contents:
                if item <> '\n':
                    tweet[item.name] = str(item.string)
            if tweet:
                tweets.append(tweet)
    return tweets

def retrieve_data(user):
    'simple http get and read'
    import urllib2
    reply = urllib2.urlopen("https://api.twitter.com/1/statuses/user_timeline.xml?contributor_details=0&trim_user=1&count=100&screen_name=%s" % user)
    data = reply.read()
    return data

def main():
    'entrance to data retrieval, parsing, analyzing and publishing'
    data = retrieve_data('chengdujin')
    tweets = parse_and_store(data)
    candidates = analyze_tweets(tweets)
    publish_candidates('chengdujin', candidates)

if __name__ == '__main__':
    main()
