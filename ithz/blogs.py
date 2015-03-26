from google.appengine.api import memcache
from datetime import datetime

#from ithz.data import queryRSS, RssScheduledModel
from ithz.lib import feedparser
from ithz.template import getTemplate

def getBlog(id,page=0):
    v = {}
    tr = getTemplate("controls/blog",v)
    return tr

def addBlog(id):
    pass
