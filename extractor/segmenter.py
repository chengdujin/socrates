#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# this script serves to segment chinese and 
# english sentences
# 
# @author Yuan JIN
# @contact chengdujin@gmail.com
# @since 2012.03.07
# @latest 2012.03.07
#

import string
import urllib2
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')


# CONSTANTS
# segmentation
WEB_SERVICE_SEG = u'http://jkx.fudan.edu.cn/fudannlp/seg/%s'
# keywords
WEB_SERVICE_KEY = u'http://jkx.fudan.edu.cn/fudannlp/key/%s'

# Stop words
CHINESE_UNWANTED = '！￥（）【】、‘’“”；：？。，《》啊阿哎哎呀哎哟唉俺俺们按按照吧吧哒把罢了被本本着比比方比如鄙人彼彼此边别别的别说并并且不比不成不单不但不独不管不光不过不仅不拘不论不怕不然不如不特不惟不问不只朝朝着趁趁着乘冲除除此之外除非除了此此间此外从从而打待但但是当当着到得的的话等等等地第叮咚对对于多多少而而况而且而是而外而言而已尔后反过来反过来说反之非但非徒否则嘎嘎登该赶个各各个各位各种各自给根据跟故故此固然关于管归果然果真过哈哈哈呵和何何处何况何时嘿哼哼唷呼哧乎哗还是还有换句话说换言之或或是或者极了及及其及至即即便即或即令即若即使几几时己既既然既是继而加之假如假若假使鉴于将较较之叫接着结果借紧接着进而尽尽管经经过就就是就是说据具体地说具体说来开始开外靠咳可可见可是可以况且啦来来着离例如哩连连同两者了临另另外另一方面论嘛吗慢说漫说冒么每每当们莫若某某个某些拿哪哪边哪儿哪个哪里哪年哪怕哪天哪些哪样那那边那儿那个那会儿那里那么那么些那么样那时那些那样乃乃至呢能你你们您宁宁可宁肯宁愿哦呕啪达旁人呸凭凭借其其次其二其他其它其一其余其中起起见起见岂但恰恰相反前后前者且然而然后然则让人家任任何任凭如如此如果如何如其如若如上所述若若非若是啥上下尚且设若设使甚而甚么甚至省得时候什么什么样使得是是的首先谁谁知顺顺着似的虽虽然虽说虽则随随着所所以他他们他人它它们她她们倘倘或倘然倘若倘使腾替通过同同时哇万一往望为为何为了为什么为着喂嗡嗡我我们呜呜呼乌乎无论无宁毋宁嘻吓相对而言像向向着嘘呀焉沿沿着要要不要不然要不是要么要是也也罢也好一一般一旦一方面一来一切一样一则依依照矣以以便以及以免以至以至于以致抑或因因此因而因为哟用由由此可见由于有有的有关有些又于于是于是乎与与此同时与否与其越是云云哉再说再者在在下咱咱们则怎怎么怎么办怎么样怎样咋照照着者这这边这儿这个这会儿这就是说这里这么这么点儿这么些这么样这时这些这样正如吱之之类之所以之一只是只限只要只有至至于诸位着着呢自自从自个儿自各儿自己自家自身综上所述总的来看总的来说总的说来总而言之总之纵纵令纵然纵使遵照作为兮呃呗咚咦喏啐喔唷嗬嗯嗳' 
ENGLSIH_UNWANTED = string.punctuation + string.whitespace
UNWANTED = CHINESE_UNWANTED + ENGLSIH_UNWANTED 

def segment(collection):
    'segmentation based on fudannlp web services'
    'collection is a list of media.Tweet instances'
    import media

    for id, item in enumerate(collection):
        if isinstance(item, media.Tweet):
            old_chinese = ' '.join(item.chinese) # data in list are unicode 
            #old_chinese = item # test code
            if old_chinese and len(old_chinese) > 2:
                con = urllib2.urlopen(WEB_SERVICE_SEG % old_chinese)
                web_data = con.read().split(' ')[1:]
                new_chinese = []
                
                for segment in web_data:
	            segment = segment.strip()
                    if not segment in UNWANTED:
                        # duplicated words should be tolerated
		        if segment.isalpha():
                            item.latin.append(segment.decode('utf-8'))
                        else:
                            new_chinese.append(segment.decode('utf-8'))
	        item.chinese = new_chinese
		print str(id+1), ','.join(new_chinese) 
    return collection

if __name__ == '__main__':
    collection = [u'就如03年5分钟,被拒绝【美签】的Google，美国人这次也很快']
    segment(collection)
