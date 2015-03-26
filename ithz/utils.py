# -*- coding: utf-8 -*-
import logging, traceback
from urllib import quote
from array import array
from random import randrange
from re import compile as re_compile, MULTILINE as re_MULTILINE
from time import time
from inspect import stack
from ithz.lib.slimmer.slimmer import slimmer


from google.appengine.api import memcache
import ithz.db_log as db_log
db_log.patch_appengine()

# Aux classes
class XTimer(object):
    def __init__(self):
        self.l = []
        self.push(2)
        
    def __call__(self):
        self.push(2)
        return self  
        
    def push(self,n=1):
        self.l.append((time(),stack()[n][1:4]))
        
    def lifeTime(self,n=None):
        '''
        b=self.l[0][0]
        for i in self.l:
            print i[0]-b,i[1]
            b=i[0]
        print time()-self.l[-1][0],"END"
        '''
        if n==None:
            return time()-self.l[0][0]
        else:
            return round(time()-self.l[0][0],n)
              
class varCacheItem(object):
    ''' Complex and optimum memcache wrapper '''
    def __init__(self,id):
        self.id = id
        self.__vars = {}
        self.__memget__()

    def __getitem__(self,i):
        if self.__vars.has_key(i):
            return self.__vars[i]
        return None

    def __setitem__(self,i,j):
        self.__vars[i] = j
        self.__memput__()
        
    def __memput__(self):
        memcache.set(self.id,self.__vars)
        
    def __memget__(self):
        try:
            cache = memcache.get(self.id)
        except:
            memcache.flush_all()
            cache=None
            
        if cache is not None:
            self.__vars = cache.copy()

    def keys(self):
        return self.__vars.keys()
    
    def values(self):
        return self.__vars.values()
    
    def clear(self,i=None):
        if i is None:
            self.__vars={}
        else:
            self.__vars.pop(i,None)
        self.__memput__()

class __VarCache(object):
    ''' VarCacheItems manager '''
    __vars = {}
    __keys = []

    def __getitem__(self,i):
        if self.__vars.has_key(i):
            return self.__vars[i]
        return None
    
    def __setitem__(self,i,j):
        self.__vars[i] = j
        if not self.has_key(i):
            self.__keys.append(i)
            
    def has_key(self,i):
        return self.__keys.__contains__(i)
        
varCache = __VarCache()

class Glass(dict):
    ''' Generic extendable class defined by diccionary '''
    def __getattribute__(self,i):
        if i[0:2] == "__":
            return dict.__getattribute__(self,i)
        elif self.__contains__(i):
            return self.__getitem__(i)
        else:
            return None
    
    def __setattr__(self,i,j):
        if i[0:2] == "__":
            dict.__setattr__(self,i,j)
        else:
            self.__setitem__(i,j)

# Aux functions
def isReal(string):
    ''' Check if string represents an integer, positive or negative '''
    if string.count("-"):
        try:
            int(string)
            return True
        except:
            return False
    else:
        return string.isdigit()
        
def isText(object):
    return isinstance(object, unicode) or isinstance(object, str)

def u(txt):
    ''' Parse any basestring (ascii str, encoded str, or unicode) to unicode '''
    if isinstance(txt,unicode):
        return txt
    else:
        for i in ["utf-8","utf-16"]:
            try:
                return unicode(txt,i)
            except:
                pass
        return unicode("")

__html_scaping=(("&","&amp;"),(">","&gt;"),("<","&lt;"),("\"","&quot;"),("'","&apos;")) # Ampersant first!
__html_unescaping=((">","&gt;"),("<","&lt;"),("\"","&quot;"),("'","&apos;"),("&","&amp;")) # Ampersant last!

def htmlEscape(string,safe=False):
    toreturn = unicode(string)
    for x,y in __html_scaping:
        if x in toreturn:
            toreturn = toreturn.replace(x,y)
    return toreturn

def htmlUnescape(string):
    toreturn = unicode(string)
    for x,y in __html_unescaping:
        if y in toreturn:
            toreturn = toreturn.replace(y,x)
    return toreturn

def hasHTML(txt):
    for x in ("<",">"):
        if x in txt:
            return True
    return False
    
__normeolre = re_compile("\r\n|\r|\n", re_MULTILINE)
def normalizeEOL(txt):
    return __normeolre.sub("\n",txt)
    
def escapeEOL(txt,repl="\\\\n"):
    return __normeolre.sub(repl,txt)

def tagStrip(html):
    ''' Strips white spaces and EOL between tags '''
    return slimmer(html)
    '''
    Old implementation
    for j in ("> ","\n"," <"):
        if j in html:
            total = []
            tmp = []
            btag = False
            for i in html:
                if btag:
                    tmp.append(i)
                    if not i in ("\r","\n"," "):
                        if i=="<":
                            total.append(i)
                        else:
                            total.extend(tmp)
                        tmp = []
                        btag = False
                else:
                    total.append(i)
                    if i==">":
                        btag = True
            return "".join(total)
    return html
    '''

__p = re_compile("<[a-zA-Z\/][^>]*>")
def removeHTML(html):
    return "".join(__p.split(html))

def isSafe(string):
    try:
        return quote(string,safe="")==string
    except:
        return False

def safeURL(url,asumeSafe=False,withGetParams=False):
    prepend=""
    if url[:7]=="http://":
        url = url[7:]
        prepend = "http://"
    elif url[:6]=="ftp://":
        url = url[6:]
        prepend = "ftp://"
    
    if asumeSafe:
        return prepend + htmlEscape(url)
    elif withGetParams:
        a = 255
        for i in "?$&":
            b=url.find(i)
            if -1 < b < a:
                a = b
        if a != None:
            return prepend + quote(url[:a]) + htmlEscape(url[a:])
    
    return prepend + quote(url)

__rChars = "abcdefghijklmnopqrstuvwxyz0123456789"
__nrChars = len(__rChars)
def randomSafeString(size):
    n = array('c',[__rChars[0]]*size)
    for i in xrange(size):
        n[i] = __rChars[randrange(0,__nrChars)]
    return n.tostring()

def formatByteSize(size):
    tr = "%g iB" % size
    if size > 1024:
        for i in ("KiB","MiB"):
            size = size/1024.
            tr = "%g %s" % (round(size,2),i)
            if size < 1024:
                break
    return tr
  
class __webCache(object):
    __ns = "pagecache"
    __index = "pagecache_index"
    __cached = None
    def __init__(self):
        c = memcache.get(self.__index)
        if c:
            self.__cached = c.split("#")
        
    def __id(self, rel, section, level):
        return "%s/%s/%s/%d" % ( self.__ns, rel, section, level )
    
    def get_page(self, rel, section, level):
        id = self.__id(rel, section, level)
        if id in self.__cached:
            memcache.get(id)
        
    def set_page(self, rel, section, level, page):
        memcache.set(self.__id(rel, section, level), page)
        
    def rem_section(self, section):
        pass
        
    def rem_release(self, rel):
        pass
        
    def getCachedItems(self):
        return self.__cached
        
        
webCache = __webCache()

def DEBUG(txt):
    logging.info("\n >>> %s" % txt)
    
def ERROR(e):
    logging.error("\n >>> %s \n > %s" % (", ".join(e.args), "\n > ".join(["%s : %d" % (i[0],i[1]) for i in traceback.extract_stack()[:-2]]) ) )
