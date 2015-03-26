from ithz.fetchrss import getRSS
from ithz.blogs import getBlog
from ithz.utils import isText, DEBUG
import re

rops = re.MULTILINE|re.DOTALL
regs = (
    (re.compile("\[[ ]*(rss|RSS)[ ]+\\\"(.+)\\\"([ ]+(\d+))?[ ]*\]((.*)\[[ ]*(endrss|ENDRSS)[ ]*\])?",rops),"rss"),
    (re.compile("\[[ ]*(comment|COMMENT)[ ]*\](.*)\[[ ]*(endcomment|ENDCOMMENT)[ ]*\]",rops),"comment"),
    (re.compile("\[[ ]*(link|LINK)[ ]+(\\\"(.+)\\\"[ ]+\\\"(.+)\\\"|\\\"(.+)\\\")[ ]*\]((.*)\[[ ]*(endlink|ENDLINK)[ ]*\])?",rops),"link"),
    )

class Inflate(object):
    def __init__(self, txt, context_vars):
        self.release = context_vars["release"]
        self.txt = txt
        self.context = context_vars
        
        for i in regs:
            self.txt = i[0].sub( self.__getattribute__("cback_%s" % i[1]), self.txt )
        
    def cback_rss(self, m):
		#[RSS "http://source.com/rss"]<b>Optional fallback HTML</b>[ENDRSS]
        #(u'rss', u'http://spayder26.blogspot.com/feeds/posts/default', None, None, u'ERROR[endrss]', u'ERROR', u'endrss')
        g = m.groups()
        try:
            a = getRSS(g[1])
            if isText(a):
                return a
        except:
            pass
        if g[4]:
            return g[5]
        return self.release.str.rss_orig_error
        
    def cback_comment(self, m):
		#[COMMENT]Commented text won't be included on client page unlinke HTML comments[ENDCOMMENT]
        return ""
        
    def cback_link(self, m):
		#[LINK "/en/section" "title"]This is a link text[ENDLINK]
        g = m.groups()
        href = g[2] or g[4]
        title = g[3]
        attrs=[]
        if href:
            attrs.append("href=\"%s\"" % href)
        if title:
            attrs.append("title=\"%s\"" % title)
        if g[5]:
            txt = g[6]
        else:
            txt = href
        DEBUG(attrs)
        return "<a %s>%s</a>" % (" ".join(attrs), txt)
            
    def get(self):
        return self.txt
        
def do(txt, release):
    c = Inflate(txt, release)
    return c.txt
