from google.appengine.api import memcache
from datetime import datetime

from ithz.data import queryRSS, RssScheduledModel
from ithz.lib import feedparser
from ithz.template import getTemplate

def parsefeed(url):
    try:
        d = feedparser.parse(url)
        if d.feed:
            for i in d.entries:
                i.published_datetime = datetime(*i.published_parsed[:7])
            return getTemplate("controls/fetchedrss",d)
    except:
        pass
    return None

def newRSS(url):
    html = parsefeed(url)
    if html is not None:
        RssScheduledModel(url=url,content=html).put()
    return html

def refreshRSS():
    for i in queryRss():
        html = parsefeed(i.url)
        if html is not None:
            memcache.delete("getrss_cache/%s" % i.url)
            i.content = html
            i.put()

def getRSS(url):
    id = "getrss_cache/%s" % url
    a = memcache.get(id)
    if not a:
        #b = queryRSS(url)
        b = False
        if b:
            a = b.content
        else:
            a = parsefeed(url)
            if not a:
                return None
        memcache.set(id, a, 43200) # 43200 seconds is 12 hours
    return a
