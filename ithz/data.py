# -*- coding: utf-8 -*-
from google.appengine.ext import db
from google.appengine.api import memcache
import ithz.utils as utils

# Data Models
class SectionModel(db.Model):
    parentid = db.StringProperty() # Empty on parent sections
    id = db.StringProperty(required=True) # Section id (used on url) < 500 char
    link = db.StringProperty(required=True) # Link text < 500 char
    description = db.StringProperty() # < Description < 500 char
    content = db.TextProperty() #HTML Code
    priority = db.IntegerProperty(default=0)
    author = db.UserProperty()
    lastdate = db.DateTimeProperty(auto_now_add=True)
    level = db.IntegerProperty(default=1)
    visibility = db.IntegerProperty(default=0)
    timestamp = db.DateTimeProperty(auto_now=True)
    
class BlogModel(db.Model):
    parentid = db.StringProperty() # Empty on parent sections
    id = db.StringProperty(required=True) # Section id (used on url) < 500 char
    link = db.StringProperty(required=True) # Link text < 500 char
    description = db.StringProperty() # < Description < 500 char
    header = db.TextProperty()
    footer = db.TextProperty()
    counter = db.IntegerProperty(default=0)
    priority = db.IntegerProperty(default=0)
    author = db.UserProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    level = db.IntegerProperty(default=1)
    visibility = db.IntegerProperty(default=0)

class BlogEntryModel(db.Model):
    blog = db.ReferenceProperty(reference_class=BlogModel)
    id = db.StringProperty(required=True) # Section id (used on url) < 500 char
    title = db.StringProperty(required=True) # Link text < 500 char
    content = db.TextProperty()
    author = db.UserProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    visibility = db.IntegerProperty(default=0)
    timestamp = db.DateTimeProperty(auto_now=True)

class UserModel(db.Model):
    user = db.UserProperty()
    level = db.IntegerProperty(default=0)
    date = db.DateTimeProperty(auto_now_add=True)
    timestamp = db.DateTimeProperty(auto_now=True)

class AuxCounterModel(db.Model):
    ''' Data counters '''
    id = db.StringProperty()
    count = db.IntegerProperty(default=0)
    timestamp = db.DateTimeProperty(auto_now=True)
    
class AppConfigModel(db.Model):
    ''' App config db '''
    id = db.StringProperty()
    value = db.StringProperty()
    timestamp = db.DateTimeProperty(auto_now=True)

class SectionHistoryModel(db.Model):
    ''' Section history '''
    section = db.ReferenceProperty(reference_class=SectionModel)
    datetime =  db.DateTimeProperty(auto_now_add=True)
    user = db.UserProperty()
    
    #contentdiff 
    changeids = db.ListProperty(int)
    timestamp = db.DateTimeProperty(auto_now=True)
    ''' Types of changes done:
    0 . other (unknown)
    1 . parentid
    2 . id
    3 . link
    4 . description
    5 . content
    6 . priority
    7 . editability (level)
    8 . owner (author)
    9 . visibility (level)
    '''

class FileModel(db.Model):
    id = db.StringProperty()
    mime = db.StringProperty()
    data = db.BlobProperty()

class UserFileModel(db.Model):
    id = db.StringProperty()
    name = db.StringProperty()
    user = db.UserProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    file = db.ReferenceProperty(FileModel)
    size = db.IntegerProperty(default=0)
    
class UserImageFileModel(db.Model):
    # Duplicated for faster queries
    id = db.StringProperty()   
    name = db.StringProperty()
    user = db.UserProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    size = db.IntegerProperty(default=0)
    file = db.ReferenceProperty(FileModel)
    thumbnail = db.BlobProperty() #100x100
    
# For cron
class RssScheduledModel(db.Model):
    url = db.StringProperty()
    content = db.TextProperty()
    
def queryRSS(id=None):
    if id:
        return RssScheduledModel.gql("WHERE id = :1",id).get()
    else:
        return RssScheduledModel.fetch(100)

# Queries
def queryFirstSection(root,user):
    return SectionModel.gql("WHERE parentid = :1 AND visibility in :2 ORDER BY priority ASC LIMIT 1", root, user.getSectionVisible()).get()
    
def queryRootSections(root,user):
    if type(root)==list:
        return SectionModel.gql("WHERE parentid in :1 AND visibility in :2 ORDER BY priority ASC", root, user.getSectionVisible())
    else:
        return SectionModel.gql("WHERE parentid = :1 AND visibility in :2 ORDER BY priority ASC", root, user.getSectionVisible())
        
def countSectionsByVisibility(v):
    return db.GqlQuery("SELECT * FROM SectionModel WHERE visibility = :1", v).count()
    
def countBlogsByVisibility(v):
    return db.GqlQuery("SELECT * FROM BlogModel WHERE visibility = :1", v).count()

def queryAllSections(offset,num,user):
    if offset == 0:
        return db.GqlQuery("SELECT * FROM SectionModel WHERE visibility in :1 ORDER BY priority ASC LIMIT %d" % num,user.getSectionVisible())
    else:
        return db.GqlQuery("SELECT * FROM SectionModel WHERE visibility in :1 ORDER BY priority ASC LIMIT %d , %d " % (offset,num),user.getSectionVisible())

def queryAllBlogs(offset,num,user):
    if offset == 0:
        return db.GqlQuery("SELECT * FROM BlogModel WHERE visibility in :1 ORDER BY priority ASC LIMIT %d" % num,user.getSectionVisible())
    else:
        return db.GqlQuery("SELECT * FROM BlogModel WHERE visibility in :1 ORDER BY priority ASC LIMIT %d , %d " % (offset,num),user.getSectionVisible())

def querySectionById(id,user):
    r = SectionModel.gql("WHERE id = :1 LIMIT 1", id).get()
    if r==None or r.visibility not in user.getSectionVisible():
        return None
    return r

def queryAllUsers(offset,num):
    if offset == 0:
        return db.GqlQuery("SELECT * FROM UserModel ORDER BY user ASC LIMIT %d" % num)
    else:
        return db.GqlQuery("SELECT * FROM UserModel ORDER BY user ASC LIMIT %d , %d " % (offset,num))
    
def queryFile(id):
    return FileModel.gql("WHERE id = :1", id).get()

def queryUserFile(id):
    return UserFileModel.gql("WHERE id = :1", id).get()

def queryImageFile(id):
    return UserImageFileModel.gql("WHERE id = :1", id).get()

def queryAllFiles(user=None,offset=0,num=10):
    if user == None:
        if offset == 0:
            return db.GqlQuery("SELECT * FROM UserFileModel ORDER BY user, date DESC LIMIT %d" % num)
        else:
            return db.GqlQuery("SELECT * FROM UserFileModel ORDER BY user, date DESC LIMIT %d , %d" % (offset, num) )
    else:
        if offset == 0:
            return db.GqlQuery("SELECT * FROM UserFileModel WHERE user = :1 ORDER BY date DESC LIMIT %d" % num, user.ref)
        else:
            return db.GqlQuery("SELECT * FROM UserFileModel WHERE user = :1 ORDER BY date DESC LIMIT %d , %d" % (offset, num), user.ref)
        
def queryAllImageFiles(user=None,offset=0,num=10):
    if user == None:
        if offset == 0:
            return db.GqlQuery("SELECT * FROM UserImageFileModel ORDER BY user, date DESC LIMIT %d" % num)
        else:
            return db.GqlQuery("SELECT * FROM UserImageFileModel ORDER BY user, date DESC LIMIT %d , %d" % (offset, num) )
    else:
        if offset == 0:
            return db.GqlQuery("SELECT * FROM UserImageFileModel WHERE user = :1 ORDER BY date DESC LIMIT %d" % num, user.ref)
        else:
            return db.GqlQuery("SELECT * FROM UserImageFileModel WHERE user = :1 ORDER BY date DESC LIMIT %d , %d" % (offset, num), user.ref)

def getUserModel(user):
    return UserModel.gql("WHERE user = :1 LIMIT 1",user).get()

def getHistoryBySection(section):
    return SectionHistoryModel.gql("WHERE section = :1", section)

# Query wrappers
class QueryMenuItem(object):
    def __init__(self, id, parentid, link, description, visibility):
        self.id = id
        self.parentid = parentid
        self.link = link
        self.description = description
        self.visibility = visibility

def queryMenuitems(parentid,user):
    # Great MenuItem by parentid optimizer
    toreturn = []
    vlvl = user.getSectionVisible()
    cache = None
    if utils.varCache.has_key("menuitems"):
        if type(parentid)==list:
            cache = []
            for i in parentid:
                item = utils.varCache["menuitems"][i]
                if item == None:
                    cache = None
                    break
                else:
                    cache.extend(item)
        else:
            cache = utils.varCache["menuitems"][parentid]
    else:
        utils.varCache["menuitems"] = utils.varCacheItem("menuitems_cache")
            
    if cache==None:
        if type(parentid)==list:
            icache = {}
            for i in parentid:
                icache[i] = []
            r = SectionModel.gql("WHERE parentid in :1 ORDER BY priority ASC", parentid)
            for i in r:
                item = QueryMenuItem(i.id, i.parentid, i.link, i.description, i.visibility)
                icache[i.parentid].append(item)
                if i.visibility in vlvl:
                    toreturn.append(item)
            for i in parentid:
                utils.varCache["menuitems"][i] = icache[i]

        else:
            cache = []
            r = SectionModel.gql("WHERE parentid = :1 ORDER BY priority ASC", parentid)
            for i in r:
                item = QueryMenuItem(i.id, i.parentid, i.link, i.description, i.visibility)
                cache.append(item)
                if i.visibility in vlvl:
                    toreturn.append(item)
            
            utils.varCache["menuitems"][parentid] = cache

    else:
        for i in cache:
            if i.visibility in vlvl:
                toreturn.append(i)
    
    return toreturn    

# Data counter
class __counter(object):       
    ns = "counter" 
    def __gfm(self,id):
        ''' Gets from datastore any entity with id '''
        return AuxCounterModel.gql("WHERE id = :1 LIMIT 1",id).get()
    
    def __com(self,id,count=0):
        ''' Instantiate a new entity with id and count '''
        return AuxCounterModel(id=id,count=count)
    
    def __getitem__(self,y):  
        ''' Gets a counter with given id. Counter[ str(id) ] '''
        v = memcache.get(y,namespace=self.ns)
        if v is None:
            qu = self.__gfm(y)
            if qu:
                v = qu.count
            else:
                v = 0
            memcache.set(y,v,namespace=self.ns) 
        return v
            
    def __setitem__(self,i,j):
        ''' Set a counter with given id. Counter[ str(id) ] = int(j) '''     
        if type(j) in (int,long):
            qu = self.__gfm(i)
            if qu:
                qu.count = j
            else:
                qu = self.__com(i,j)
            qu.put()
            memcache.set(i,j,namespace=self.ns)
            
    def setMulti(self,d):
        ''' Set counters with given ids as dict. Counter.setMulti({dictionary}) '''     
        for i in d.values():
            if not type(i) in (int,long):
                return None
        memcache.set_multi(d,namespace=self.ns)
        nid = d.keys()
        r = AuxCounterModel.gql("WHERE id in :1",nid)
        for i in r:
            nid.remove(i.id)
            i.count = int(d[i.id])
            i.put()
        if nid:
            tc = []
            for i in nid:
                tc.append(self.__com(i,d[i]))
            db.put(tc)
            
    def getMulti(self,l):
        ''' Get a dict of counters from given id list. '''                
        tr = dict(memcache.get_multi(l,namespace=self.ns))
        gk = tr.keys()
        if len(l) > len(gk):
            l = l[:]
            for i in gk:
                l.remove(i)
            d = {}
            r = AuxCounterModel.gql("WHERE id in :1",l)
            for i in r:
                l.remove(i.id)
                tr[i.id] = i.count
                d[i.id] = i.count
            memcache.set_multi(d,namespace=self.ns)
            for i in l:
                tr[i] = 0

        return tr
            
counter = __counter()
