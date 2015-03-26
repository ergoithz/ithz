# -*- coding: utf-8 -*-
from google.appengine.ext import db
from google.appengine.api import images
from google.appengine.api.memcache import flush_all

from urllib import unquote
from datetime import datetime
from re import compile as re_compile

from ithz.utils import *
from ithz.data import *
from ithz.appdata import APPCONFIG

import ithz.security as security

re_validSectionId = re_compile("^(?!blog).+$")
class Post(object):
    def __init__(self,request,section,arg):
        user = security.User()
        self.section = section
        self.arg = arg
        self.contexto = {"user":user}
        self.errors = []
        if section in ("new","edit","remove"):
            errorlist = []
            if section=="new":
                errorlist.append((not user.getSectionAdd(),"You're not allowed to doing that"))

            if section in ("new","edit"):
                parentid = request.get("parentid").strip()
                newid = request.get("id").strip()
                linktext = htmlEscape(request.get("link").strip())
                priority = request.get("priority").strip()
                editability = request.get("editability")
                visibility = request.get("visibility")
                description = htmlEscape(request.get("description").strip())
                content = request.get("content").strip()
                
                roots = [i.code for i in APPCONFIG["releases"]]
                rootsections = [i.id for i in queryRootSections(roots,user)]
                unlisted = [""]
                
                errorlist.extend([
                    (not re_validSectionId.match(newid),"Section id is not valid, please, replace it"),
                    (not newid,"You must define an unique identifier"),
                    (not linktext,"You must define link text"),
                    (not isReal(priority),"Priority must be a number"),
                    (not editability.isdigit(),"Editability not valid"),
                    (not visibility.isdigit(),"Visibility not valid"),
                    (not isSafe(newid),"Id must be an alphanumeric value (but also \".\", \"_\" and \"-\" )"),
                    (not parentid in (roots+rootsections+unlisted),"Cannot put section on given place, choose other parent"),
                    (len(newid) > 50,"Id is too large, max size is 50"),
                    (0 < len(newid) < 5,"Id is too small, it should be bigger than 5 characters"), # > 0 because we're checking newid as bool above.
                    (len(linktext) > 300,"Link text is too large, max size is 300"),
                    (len(description) > 500,"Description is too large, max size is 500"),          
                    ])
            
            if section == "new" or (section == "edit" and arg != newid):
                errorlist.append((querySectionById(newid,user)!=None,"There is other section with the same id"))
            
            qu = None
            if section in ("edit","remove"):
                qu = querySectionById(arg,user)
                errorlist.append((qu==None,"There isn't any section with id %s." % arg))
                errorlist.append((qu.author != user.ref and not qu.level in user.getSectionEdit(),"You're not allowed to doing that"))
                                            
            for x,y in errorlist:
                if (x):
                    self.errors.append(y)
            
            if not self.errors and section in ("new","edit"):
                editability = int(editability)
                edit_levels = user.getSectionEdit()
                over = user.getLevelOver()
                if over:
                    edit_levels.append(over)
                if editability not in edit_levels:
                    self.errors.append("The selected section edition level isn't valid")
                    
                visibility = int(visibility)
                if visibility not in user.getSectionVisible():
                    self.errors.append("The selected section visibility level isn't valid")
                    
                priority = int(priority)
                #TODO: only admin can change priority

            if not self.errors:
                if section=="edit":
                    changes = []
                    if qu.parentid != parentid:
                        qu.parentid = parentid
                        changes.append(1)
                        
                    if qu.id != newid:
                        qu.id = newid
                        changes.append(2)
                        
                    if qu.link != linktext: 
                        qu.link = linktext
                        changes.append(3)
                        
                    if qu.description != description:
                        qu.description = description
                        changes.append(4)
                    
                    if qu.content != content:
                        qu.content = content
                        changes.append(5)
                        
                    priority = int(priority)
                    if qu.priority != priority:
                        qu.priority = priority
                        changes.append(6)
                        
                    if qu.level != editability:
                        qu.level = editability
                        changes.append(7)
                        
                    if qu.visibility != visibility:
                        qu.visibility = visibility
                        o = ["%d/section" % i for i in [qu.visibility,visibility]]
                        c = dict(counter.getMulti(o))
                        c[o[0]] -= 1
                        c[o[1]] += 1
                        counter.setMulti(c)
                        counter["%d/section" % visibility] += 1
                        changes.append(9)
                        
                    modification_date = datetime.now()
                    #qu.author = user.ref will be managed by history algorythm
                    qu.lastdate = modification_date
                    
                    db.put(qu)
                    db.put(SectionHistoryModel(section=qu,date=modification_date,user=user.ref))
                    self.arg = newid

                    parent=parentid
                elif section=="new":
                    new = SectionModel(
                        parentid = parentid,
                        id = newid,
                        link = linktext,
                        description = description,
                        content = content,
                        author = user.ref,
                        visibility = visibility,
                        priority = priority,
                        level = editability
                        )
                    db.put(new)
                    counter["%d/section" % visibility] += 1
                    parent = parentid
                elif section=="remove":
                    while True:
                        hist = getHistoryBySection(qu)
                        if hist.count(1):
                            db.delete(hist)
                        else:
                            break

                    parent = qu.parentid
                    db.delete(qu)
                    counter["%d/section" % visibility] -= 1
                self.contexto["formsuccess"] = True
                
                if varCache.has_key("menuitems"):
                    varCache["menuitems"].clear() # Clear the section cache
            else:
                self.contexto.update({
                    "parentid" : parentid,
                    "id" : newid,
                    "link" : linktext,
                    "description" : request.get("description").strip(),
                    "content" : request.get("content").strip(),
                    "author" : user.ref,
                    "priority" : priority,
                    "level" : int(request.get("editability")),
                })
        elif section in ("newuser","edituser","removeuser"):
            errorlist = []
            if section in ("newuser","edituser"):
                edomains = ("@gmail.com",)
                email = request.get("email").strip()
                level = request.get("level").strip()
                valid = False
                for i in edomains:
                    if email[(len(i)*(-1)):] == i:
                        valid = True
                        break
                
                errorlist.extend([
                    (not valid, "Email provider isn't valid. Currently only gmail is suported"),
                    (not level.isdigit(), "Invalid level value")
                    ])
            
            qu = None
            if section in ("edituser","removeuser"):
                qu = getUserModel(security.getUserRef(unquote(arg)))
                errorlist.append(((not qu.level in user.getUserEdit()),"You're not allowed of doing that"))
            
            for x,y in errorlist:
                if (x):
                    self.errors.append(y)
            
            if section in ("newuser","edituser") and not self.errors:
                level = int(level)
                if not level in user.getUserEdit():
                    self.errors.append("Level value is not valid")
            
            if not self.errors:
                if section=="newuser":
                    new = UserModel(user=security.getUserRef(email),level=level)
                    db.put(new)
                    counter["user"] += 1
                elif section=="edituser":
                    qu.user = security.getUserRef(email)
                    qu.level = level
                    db.put(qu)
                    self.arg = email
                elif section=="removeuser":
                    db.delete(qu)
                    counter["user"] -= 1
                self.contexto["formsuccess"] = True
            else:
                self.contexto.update({
                    "email" : email,
                    "level" : level,
                    })
        elif section=="upload":
            if user.getFileAdd():
                data = request.get("file")
                if data:
                    blob = db.Blob(data)
                    mime = request.body_file.vars['file'].headers['content-type']
                    id = self.__genId(queryFile,20)
                    size = len(blob)

                    file = FileModel()
                    file.id = id
                    file.mime = mime
                    file.data = blob
                    file.put()
                    
                    userfile = UserFileModel()
                    userfile.id = id
                    userfile.name = request.body_file.vars['file'].filename
                    userfile.user = user.ref
                    userfile.file = file
                    userfile.size = size
                    userfile.put()
                    
                    if mime in APPCONFIG["image_mimes"]:
                        thumbnail = None
                        if mime in APPCONFIG["gae_image_mimes"]:
                            preview = images.Image(data)
                            preview.resize(width=100, height=100)
                            thumbnail = db.Blob(preview.execute_transforms(output_encoding=images.PNG))
                        
                        imagefile = UserImageFileModel()
                        imagefile.id = id
                        imagefile.name = request.body_file.vars['file'].filename
                        imagefile.user = user.ref
                        imagefile.file = file
                        imagefile.size = size
                        imagefile.thumbnail = thumbnail
                        imagefile.put()     
                    
                    counter["file"] += 1
                    self.contexto["formsuccess"] = True
                    
                else:
                    self.errors.append("No file uploaded")
            else:
                self.errors.append("User cannot upload files")
        elif section=="removefile":
            qu = queryUserFile(arg)
            if qu != None:
                if qu.user==user or user.getFileAdmin():
                    image = queryImageFile(arg)
                    if image:
                        db.delete(image)
                    db.delete(qu.file)
                    db.delete(qu)
                    counter["file"] -= 1
                    self.contexto["formsuccess"] = True
                else:
                    self.errors.append("Your user cannot perform this action")
            else:
                self.errors.append("File not found")
        elif section=="counters":
            if user.isadmin():
                try:
                    ts = {}
                    for i in user.getSectionVisible():
                        ts["%d/section" % i] = int(request.get("level_%d/section" % i))
                        ts["%d/blog" % i] = int(request.get("level_%d/blog" % i))
                    counter.setMulti(ts)
                    self.contexto["formsuccess"] = True
                except:
                    self.errors.append("Malformed post")
            else:
                self.errors.append("You cannot perform this action")
                
        if self.errors:
            self.contexto["errors"] = self.errors
        elif section=="maintenance":
            if user.isadmin():
                try:
                    if request.get("clearmem"):
                        flush_all()
                        self.contexto["formsuccess"] = True
                except:
                    self.errors.append("Malformed post")
            else:
                self.errors.append("You cannot perform this action")
        
    def __genId(self,comp,len):
        chk = True
        while chk:
            id = randomSafeString(len)
            chk = bool(comp(id))
        return id
    
class DialogPost(Post):
    def __init__(self,request,section,arg):
        if section in APPCONFIG["dialogable"]:
            Post.__init__(self,request,section,arg)
        else:
            request.error(404)
