# -*- coding: utf-8 -*-
from google.appengine.api import users
from ithz.data import *

class SectionRights(object):
    view = None # level list
    edit = None # level list
    add = False # boolean
    assign = False # boolean
    def __init__(self):
        self.view = [0]
        self.edit = []

class BlogRights(object):
    view = None # level list
    viewEntry = None
    edit = None # level list
    editEntry = None
    add = False # boolean
    addEntry = False
    assign = False # boolean
    assignEntry = False
    def __init__(self):
        self.view = [0]
        self.edit = []
        self.viewEntry = [0]
        self.editEntry = []
           
class UserRights(object):
    edit = None # level list
    list = False # boolean
    add  = False # boolean
    def __init__(self):
        self.edit = []

class FileRights(object):
    add = False
    admin = False
    
class ServerRights(object):
    admin = False

class __level(object):
    def __init__(self,id,one,more):
        self.id = id
        self.__one = one
        self.__more = more
        self.section = SectionRights()
        self.blog = BlogRights()
        self.user = UserRights()
        self.file = FileRights()
        self.server = ServerRights()
        
    def getName(self,n=0):
        if n:
            return self.__more
        return self.__one

levels = [
    __level(0,"public user","public users"),
    __level(1,"admin", "admins"),
    __level(2,"moderator", "moderators"),
    __level(3,"editor","editors"),
    __level(4,"registered user", "registered users"),
]
''' Due GQL limitations, level's length cannot be greater than 30

    From GQL reference:
    [...]
    Note: The IN and != operators use multiple queries behind the scenes.
    For example, the IN operator executes a separate underlying datastore
    query for every item in the list. The entities returned are a result of
    the cross-product of all the underlying datastore queries and are
    de-duplicated. A maximum of 30 datastore queries are allowed for any
    single GQL query.
    [...]
    (http://code.google.com/intl/es/appengine/docs/python/datastore/gqlreference.html)
'''

__lvl = range(1,len(levels))+[0]

# Admin
__adm = __lvl[:]
levels[1].section.view = __adm
levels[1].section.edit = __adm[:-2]
levels[1].section.add = True
levels[1].section.assign = True
levels[1].blog.view = __adm
levels[1].blog.viewEntry = __adm
levels[1].blog.edit = __adm[:-2]
levels[1].blog.editEntry = __adm[:-2]
levels[1].blog.add = True
levels[1].blog.addEntry = True
levels[1].blog.assign = True
levels[1].blog.assignEntry = True
levels[1].user.list = True
levels[1].user.add = True
levels[1].user.edit = __adm
levels[1].file.add = True
levels[1].file.admin = True
levels[1].server.admin = True

# Mod
__mod = __lvl[:-1]
levels[2].section.view = __mod
levels[2].section.edit = __mod[:-2]
levels[2].section.add = True
levels[2].section.assign = True
levels[2].blog.view = __mod
levels[2].blog.viewEntry = __mod
levels[2].blog.edit = __mod[:-2]
levels[2].blog.editEntry = __mod[:-2]
levels[2].blog.add = True
levels[2].blog.addEntry = True
levels[2].blog.assign = True
levels[2].blog.assignEntry = True
levels[2].user.list = True
levels[2].user.add = True
levels[2].user.edit = __mod
levels[2].file.add = True
levels[2].file.admin = True

# Editor
levels[3].section.view = [3, 4, 0]
levels[3].section.edit = [3]
levels[3].section.add = True
levels[3].blog.view = [3, 4, 0]
levels[3].blog.viewEntry = [3, 4, 0]
levels[3].blog.edit = [3]
levels[3].blog.editEntry = [3]
levels[3].blog.add = True
levels[3].blog.addEntry = True
levels[3].file.add = True

# Registered user
levels[4].section.view = [4, 0]
levels[4].blog.view = [4, 0]

def getLevelName(id,n=0):
    ''' Returns level name of given id. '''
    return levels[id].getName(n)

def getUserRef(email=None):
    ''' Returns user reference by its email '''
    return users.User(email)
      
class User(object):
    ''' A class that represents an application user and it's rights and properties. '''
    username = "Public user"
    email    = ""
    ref      = None

    __level = None # Level class instance

    def __init__(self,ref=None):
        level = 0
        if ref==None:
            ref = users.get_current_user()
                    
        if ref:
            self.username = ref.nickname()
            self.email = ref.email()
            self.ref = ref

            if users.is_current_user_admin():
                level = 1
            else:
                qu = getUserModel(ref)
                if qu and qu.level != 0:
                    level = qu.level
        
        self.__level = levels[level]
    
    def __eq__(self,y):
        ''' x.__eq__(y) <==> x==y '''
        return self.ref == y
        
    def getLevel(self):
        return self.__level.id
    
    # Sections
    def getSectionVisible(self):
        ''' Return list of visible section levels '''
        return self.__level.section.view[:]
    
    def getSectionEdit(self):
        ''' Return list of editable section levels '''
        return self.__level.section.edit[:]
    
    def getSectionAdd(self):
        ''' Return boolean. Can user add a section? '''
        return self.__level.section.add
    
    def getSectionAssign(self):
        ''' Return boolean. Can user reassign a section? '''
        return self.__level.section.assign
        
    # Blogs
    def getBlogVisible(self):
        ''' Return list of visible blog levels '''
        return self.__level.blog.view[:]
    
    def getBlogEdit(self):
        ''' Return list of editable blog levels '''
        return self.__level.blog.edit[:]
    
    def getBlogAdd(self):
        ''' Return boolean. Can user add a blog? '''
        return self.__level.blog.add
    
    def getBlogAssign(self):
        ''' Return boolean. Can user reassign a blog? '''
        return self.__level.blog.assign
        
    def getBlogEntryVisible(self):
        ''' Return list of visible blog levels '''
        return self.__level.blog.viewEntry[:]
    
    def getBlogEntryEdit(self):
        ''' Return list of editable blog levels '''
        return self.__level.blog.editEntry[:]
    
    def getBlogEntryAdd(self):
        ''' Return boolean. Can user add a blog? '''
        return self.__level.blog.addEntry
    
    def getBlogEntryAssign(self):
        ''' Return boolean. Can user reassign a blog? '''
        return self.__level.blog.assignEntry
        
    
    # Users
    def getUserAdd(self):
        ''' Return boolean. Can user reassign a section? '''
        return self.__level.user.add
    
    def getUserEdit(self):
        ''' Return list of editable users' levels '''
        return self.__level.user.edit[:]
    
    def getUserListing(self):
        ''' Return boolean. Can user list all users? '''
        return self.__level.user.list

    def getLevel(self):
        ''' Return level id. '''
        return self.__level.id

    def getLevelOver(self):
        ''' Return level over own level '''
        if not self.__level.id in (0, 1):
            return self.__level.id-1
        return None
    
    def getLevelName(self,n=0):
        ''' Return level verbose name. '''
        return self.__level.getName(n)
    
    # Files
    def getFileAdd(self):
        ''' Return boolean. Can user add a file? '''
        return self.__level.file.add
    
    def getFileAdmin(self):
        ''' Return boolean. Can user administrate files? '''
        return self.__level.file.admin
        
    # Server
    def getServerAdmin(self):
        ''' Return boolean. Can user flush the cache? '''
        return self.__level.server.admin
    
    # What is?
    def ispublic(self):
        ''' Returns True user is public, otherwise False '''
        return (self.__level.id == 0)
    
    def isadmin(self):
        ''' Returns True user is admin, otherwise False '''
        return (self.__level.id == 1)
    
    def ismoderator(self):
        ''' Returns True user is moderator, otherwise False '''
        return (self.__level.id == 2)
    
    def iseditor(self):
        ''' Returns True user is editor, otherwise False '''
        return (self.__level.id == 3)
    
    def isregistrered(self):
        ''' Returns True user is registered, otherwise False '''
        return (self.__level.id == 4)
