#!/home/work/python/bin/python
# -*- coding: utf-8 -*-

import memcache
from hashlib import md5
import sys

reload(sys)
sys.setdefaultencoding("UTF-8")

def main():
    mc = memcache.Client(['127.0.0.1:11211'])
    flag_flushed = False
    #while not flag_flushed:
    #    flag_flushed = mc.flush_all()
    
    input = open('/home/work/yuanj/bigrams.txt', 'r')
    entries = input.readlines()
    input.close()
    
    for entry in entries:
        entry = unicode(entry)
        sepentry = entry.split(':')
        key = md5(unicode(sepentry[0])).hexdigest()
        values = sepentry[1].split('||')
        flag_set = False
        counter_set = 0
        while not flag_set:
            if counter_set > 5:
                if not mc.get(key):
                    flag_set = mc.add(key, values, 60*60)
                    print 'Problem found in adding ' + sepentry[0] + ', but it fails'
                    if counter_set > 10:
                        break
                else:
                    ret = mc.delete(key)
                    print 'Problem found in deleting ' + sepentry[0] + ' with code ' + str(ret)
            
            if not mc.get(key):
                flag_set = mc.add(key, values, 60*60*10)
            else:
                flag_set = mc.replace(key, values, 60*60*10)
            counter_set += 1

if __name__ == '__main__':
    main()
