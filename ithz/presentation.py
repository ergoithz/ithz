# -*- coding: utf-8 -*-
from os import environ
from urllib import unquote
import operator

#from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.api import memcache

from ithz.security import getUserRef, getLevelName, User

from ithz.utils import *
from ithz.data import *
from ithz.appdata import APPCONFIG
from ithz.mimetypes import getMimeIcon
from ithz.template import getTemplate

import ithz.inflatext as inflatext
import ithz.appdata as appdata

def getRelease(context):
    release = APPCONFIG["releases"][0]
    if context.has_key("prefix") and context["prefix"] in APPCONFIG["prefixes"]:
            release = APPCONFIG["releases_by_prefix"][context["prefix"]]
    elif environ.has_key("HTTP_ACCEPT_LANGUAGE"):
        for i in environ["HTTP_ACCEPT_LANGUAGE"].split(";")[0].split(","):
            if APPCONFIG["releases_by_language"].has_key(i):
                release = APPCONFIG["releases_by_language"][i]
                break
    return release

class MenuItem(object):
    def __init__(self,text,href,alt="",selected=False):
        self.text = text
        self.href = href
        self.alt = alt
        self.selected = selected # Bool

class sectionlistItem(object):
    def __init__(self,text,id,link,edit,remove,description,parent="",author=None,date=None,):
        self.text = text
        self.id = id
        self.description = description
        self.parent = parent
        self.author = author
        self.date = date
        self.link = link
        self.edit = edit
        self.remove = remove

class userlistItem(object):
    def __init__(self, username, levelname, edit, remove,date=None):
        self.username = username
        self.levelname = levelname
        self.date = date
        self.edit = edit
        self.remove = remove

class SelectItem(object):
    def __init__(self,text="",value=""):
        self.text = text
        self.value = value

class LinkItem(object):
    def __init__(self,href):
        self.href = href

class PageItem(object):
    def __init__(self, n, text, href):
        self.n = n
        self.text = text
        self.href = href

class Image(object):
    def __init__(self, src, alt=""):
        self.src = src
        self.alt = alt

class UserFileItem(object):
    def __init__(self,id,name,remove,size,date,icon=None):
        self.name = name
        self.id = id
        self.link = fileprefix + id + "/" +name
        self.remove = remove
        self.size = size
        self.date = date
        self.icon = icon

class UserImageFileItem(object):
    def __init__(self,id,name,remove,size,date,preview=None):
        self.name = name
        self.id = id
        self.link = fileprefix + id + "/" +name
        self.remove = remove
        self.size = size
        self.date = date
        self.preview = preview

class FileItem(UserFileItem):
    def __init__(self,id ,name,remove,size,user,date,icon=None):
        UserFileItem.__init__(self, id, name,remove,size,date,icon)
        self.user = user

# Client code generation
imgpreviewprefix = "/preview/"
adminprefix = "/admin/"
dialogprefix = "/dialog/"
fileprefix = "/file/"
blogprefix = "/blog/"

newprefix = "/new"
editprefix = "/edit/"
removeprefix = "/remove/"
listprefix = "/sections/"

usernewprefix = "/newuser"
usereditprefix = "/edituser/"
userremoveprefix = "/removeuser/"
userlistprefix = "/users/"

blognewprefix = "/newblog"
blogeditprefix = "/editblog/"
blogremoveprefix = "/removeblog/"
bloglistprefix = "/blogs/"

filenewprefix = "/upload"
fileremoveprefix = "/removefile/"

defaultAdminSection = "frontpage"

class generateSection(object):
    def __init__(self,context_vars=None):
        if context_vars==None:
            context_vars = {}

        # Will change
        if context_vars.has_key("errors"):
            errors = context_vars["errors"]
        else:
            errors = []

        # Optional
        if context_vars.has_key("chronos"):
            context_vars["chronos"].push()

        # Cannot change
        if context_vars.has_key("section"):
            section = context_vars["section"]

        if context_vars.has_key("release"):
            release = context_vars["release"]
        else:
            release = getRelease(context_vars)
            context_vars["release"] = release

        if context_vars.has_key("user"):
            user = context_vars["user"]
        else:
            user = User()
            context_vars["user"] = user

        menuitems = []
        sideitems = []
        linkitems = {}
        content = None
        show_menus = not (context_vars.has_key("skip_menus") and context_vars["skip_menus"])

        prefix = "/%s/" % release.prefix
        mineparent=None
        mine = None
        if section:
            mine = querySectionById(section,user)
        else:
            mine = queryFirstSection(release.code,user)
            if mine:
                section = mine.id

        if mine and section:
            if user == mine.author or mine.level in user.getUserEdit():
                linkitems["editlink"] = LinkItem(adminprefix+release.prefix+editprefix+mine.id)

            content = inflatext.do(mine.content, context_vars)
            mineparent = mine.parentid

            if mineparent == release.code:
                mineparent = mine.id


            if mineparent != "" and show_menus:
                for i in queryMenuitems(mineparent,user):
                    sideitems.append(MenuItem(i.link,prefix+i.id,i.description,i.id==mine.id))

        if show_menus:
            for i in queryMenuitems(release.code,user):
                menuitems.append(MenuItem(i.link,prefix+i.id,i.description,i.id==mineparent))

        self.setVars(context_vars, user, linkitems, menuitems, sideitems, prefix, content, section, errors)

    def setVars(self, context_vars, user, linkitems, menuitems, sideitems, prefix, content, section, errors=None, adminSection=False):
        if errors==None:
            errors = []
        if content==None:
            errors.append("No section found")
            content = getTemplate("error",{"errors":errors})

        if user.getLevel()>0:
            menuitems.append(MenuItem("Admin","%s%s/frontpage" % (adminprefix, context_vars["release"].prefix),"Website administration options.", adminSection))

        if context_vars.has_key("chronos"):
            context_vars["chronos"].push()

        ismain = True
        for i in sideitems:
            if i.selected:
                ismain = False
                break

        self.context = context_vars
        self.user = user
        self.linkitems = linkitems
        self.menuitems = menuitems
        self.sideitems = sideitems
        self.prefix = prefix
        self.content = content
        self.section = section
        self.errors = errors
        self.ismain = ismain

    def getAjax(self):
        content = {'content': self.content, "errors": self.errors}
        content.update(self.linkitems)
        if self.section:
            section = self.section
        else:
            section = ""

        json = "{'menu':'%s','side':'%s','content':'%s','gentime':'%g','id':'%s'}" % (
            getTemplate("controls/topmenu" , {'menuitems': self.menuitems,"ismain": self.ismain}).replace("'","\\'").strip(),
            getTemplate("controls/sidemenu", {'sideitems': self.sideitems}).replace("'","\\'").strip(),
            getTemplate("controls/contentblock",content).replace("'","\\'").strip(),
            self.context["chronos"].lifeTime(4),
            section)

        return escapeEOL(tagStrip(json))

    def getMain(self):
        if self.section == None:
            self.section = ""

        username = None
        if self.user.ref:
            username = self.user.username

        langs = []
        releases = APPCONFIG["releases"]
        if len(releases)>1:
            for i in releases:
                a = LinkItem("/%s" % i.prefix)
                a.alt = i.description
                a.src = "/flags/%s.gif" % i.code
                a.hreflang = i.ref
                langs.append(a)

        #'<script type="text/javascript" src="http://www.google.com/jsapi?key=ABQIAAAAJvpqo5DaL-ArKL9ZcjWDfBSUExBnWDL53GbCbc8nidgHVfOaUBQOXM8GOtkYcZpB0rnuKRJeIcx-8Q"></script>'


        template_values = {
            'errors': self.errors,
            'JavaScripts' : (
                             '<script type="text/javascript" src="/js/main.js"></script>'
                             '<script type="text/javascript" src="/js/config.js"></script>'
                             ),
            'ismain': self.ismain,
            'logged': (username != None),
            'login': users.create_login_url(self.prefix+self.section),
            'username': username,
            'unlog': users.create_logout_url(self.prefix+self.section),
            'menuitems': self.menuitems,
            'sideitems': self.sideitems,
            'content': self.content,
            'languages' : langs,
            'gentime' : "%g" % self.context["chronos"].lifeTime(4),
            }
        template_values.update(self.linkitems)
        return tagStrip(getTemplate("main", template_values))

class generateAdminSection(generateSection):
    def __init__(self,context_vars=None):
        if context_vars==None:
            context_vars = {}

        if context_vars.has_key("errors"):
            errors = context_vars["errors"]
        else:
            errors = []

        if context_vars.has_key("section"):
            section = context_vars["section"]
        else:
            section = defaultAdminSection
            context_vars["section"] = section

        if context_vars.has_key("user"):
            user = context_vars["user"]
        else:
            user = User()
            context_vars["user"] = user

        if context_vars.has_key("chronos"):
            context_vars["chronos"].push()

        if context_vars.has_key("release"):
            release = context_vars["release"]
        else:
            release = getRelease(context_vars)
            context_vars["release"] = release

        show_menus = not (context_vars.has_key("skip_menus") and context_vars["skip_menus"])

        menuitems = []
        sideitems = []
        linkitems = {}

        content = None

        prefix = "/%s/" % release.prefix
        aprefix = "%s%s/" % (adminprefix, release.prefix)
        parentid = release.code

        if user.getLevel() == 0:
            errors.append("Permission forbidden (try <a href=\"%s\">log in</a>)" % safeURL(users.create_login_url(adminprefix+section),True))
        else:
            roots = []
            if show_menus:
                roots = queryMenuitems([i.code for i in APPCONFIG["releases"]],user)
                for i in roots:
                    if i.parentid == parentid:
                        menuitems.append(MenuItem(i.link,prefix+i.id,i.description))

                sidemenu = []

                if user.getSectionAdd():
                    sidemenu.append(("new","New section","Section/subsection creation form",section=="new"))

                sidemenu.append(("sections","List sections","List all sections visible by you",section=="sections"))

                '''
                if user.getBlogAdd():
                    sidemenu.append(("newblog","New blog","Create a new blog",section=="newblog"))

                sidemenu.append(("blogs","List blog","List all blogs visible by you",section=="blogs"))
                '''

                if user.getFileAdd():
                    sidemenu.append(("upload","Upload file","Upload file",section=="upload"))
                    sidemenu.append(("userfiles","List files","List your uploaded files",section=="userfiles"))

                if user.getFileAdmin():
                    sidemenu.append(("files","List all files","List all uploaded files",section=="files"))

                if user.getUserListing():
                    sidemenu.append(("users","List users","List all users and their data",section=="users"))

                if user.isadmin():
                    sidemenu.append(("counters","Manage counters","DB entity counter's fix for maintenance",section=="counters"))
                    sidemenu.append(("maintenance","Maintenance","Common actions to maintain the site",section=="maintenance"))

                for x,y,z,w in sidemenu:
                    sideitems.append(MenuItem(y,aprefix+x,z,w))


            #text,href="javascript:",alt="",selected=False
            if section in ("new","edit","remove"):
                error = ""
                values = {
                    "form_action": adminprefix+release.prefix+"/"+section,
                    "parentids": [],
                    "editlevels": [],
                    "showlevels": [],
                    "priority" : 0
                    }

                current = None
                denied = False
                values.update(context_vars)
                if section =="remove" and values.has_key("formsuccess") and values["formsuccess"]:
                   values["backurl"]=adminprefix+release.prefix+"/sections"
                else:
                    if context_vars.has_key("subsection") and section in ("edit","remove"):
                        subsection = context_vars["subsection"]
                        datos = querySectionById(subsection,user)
                        if datos != None and (datos.level in user.getSectionEdit() or datos.author == user.ref):
                            values["form_action"] += "/"+subsection
                            current = datos.id
                            values["parentid"] = datos.parentid
                            values["id"] = current
                            values["link"] = datos.link
                            if section=="remove":
                                values["description"] = datos.description[:25]+("..."*(len(datos.description)>25))
                                scnt = removeHTML(datos.content)
                                values["content"] = scnt[:25]+("..."*(len(scnt)>25))
                                values["owned"] = (datos.author == user.ref)
                            else:
                                values["description"] = datos.description
                                values["content"] = datos.content
                            values["author"] = datos.author
                            values["priority"] = datos.priority
                            values["level"] = datos.level
                            values["showlevel"] = datos.visibility
                            values["date"] = datos.lastdate
                        else:
                            errors.append("This section doesn't exist yet or access denied.")
                            denied = True
                    elif section == "new":
                        if user.getSectionAdd():
                            if not values.has_key("id"):
                                values["id"] = randomSafeString(10)
                            if not values.has_key("level"):
                                if user.isadmin():
                                    values["level"] = user.getLevel()
                                else:
                                    values["level"] = user.getLevelOver()
                            if not values.has_key("showlevel"):
                                values["showlevel"] = 0
                        else:
                            errors.append("Access denied")
                            denied = True

                if not denied:
                    for i in APPCONFIG["releases"]:
                        values["parentids"].append(SelectItem("Root for \"%s\"" % i.name, i.code))

                    for i in roots:
                        if i.id != current:
                            values["parentids"].append(SelectItem(i.link,i.id))

                    values["parentids"].append(SelectItem("Unlisted", ""))

                    list = user.getSectionEdit()
                    try:
                        list.remove(user.getLevel())
                    except:
                        pass
                    values["editlevels"].append(SelectItem("Other %s" % user.getLevelName(1),user.getLevel()))
                    for i in list:
                        values["editlevels"].append(SelectItem(getLevelName(i,1).capitalize(),i))

                    if not user.isadmin():
                        values["editlevels"].append(SelectItem("Don't allow",user.getLevelOver()))

                    for i in user.getSectionVisible():
                        values["showlevels"].append(SelectItem(getLevelName(i,1).capitalize(),i))

                    if section in ("new","edit"):
                        content = getTemplate("editsection",values)
                    elif section == "remove":
                        values["backurl"] = adminprefix+release.prefix+"/sections"
                        content = getTemplate("removing",values)

            # users.create_logout_url("/")
            elif section == "sections":
                spp = 10 # Sections per page
                maxpages = 10 # Max pages
                page = 0 # Current page
                if context_vars.has_key("subsection") and isReal(context_vars["subsection"]) and context_vars["subsection"]>0:
                    page = int(context_vars["subsection"])-1

                offset = spp*page
                nsections = sum( counter.getMulti( ["%d/section" % i for i in user.getSectionVisible()] ).values() )
                DEBUG(counter.getMulti( ["%d/section" % i for i in user.getSectionVisible()] ))
                npages = (nsections/spp)+((nsections%spp)>0)
                if npages == 0:
                    npages = 1

                pages = []
                for i in range(npages):
                    n = i+1
                    pages.append(PageItem(n,str(n),"%s%d" % (adminprefix+release.prefix+listprefix,n)))

                sl = queryAllSections(offset,spp,user)
                overlevels = user.getSectionVisible()
                items = []
                for i in sl:
                    edit = ""
                    remove = ""
                    if i.level in overlevels or i.author == user.ref:
                        edit = adminprefix+release.prefix+editprefix+i.id
                        remove = adminprefix+release.prefix+removeprefix+i.id
                    items.append(sectionlistItem(i.link,i.id,"%s%s" % (prefix,i.id),edit,remove,i.description,i.parentid,i.author,str(i.lastdate).split(".")[0]))

                add = ""
                if user.getSectionAdd():
                    add = adminprefix+release.prefix+newprefix
                values = {
                    "page" : page+1,
                    "pagelist" : pages,
                    "items": items,
                    "spp" : spp,
                    "nsections" : nsections,
                    "add" : add
                }
                content = getTemplate("sectionlist",values)
            elif section in ("newuser","edituser","removeuser"):
                values = {
                    "form_action": "%s/%s" % (adminprefix+release.prefix,section),
                    "level" : 0,
                    "editlevels": [],
                    }

                values.update(context_vars)
                overlevels = user.getUserEdit()

                for i in overlevels:
                    values["editlevels"].append(SelectItem(getLevelName(i,0).capitalize(),i))

                if section =="removeuser" and values.has_key("formsuccess") and values["formsuccess"]:
                   values["backurl"]=adminprefix+release.prefix+"/users"
                elif section in ("edituser","removeuser"):
                    values["backurl"] = "%s/users" % (adminprefix+release.prefix)
                    subsection = unquote(context_vars["subsection"])
                    qu = getUserModel(getUserRef(subsection))
                    values["form_action"] += "/"+subsection
                    if qu and qu.level in overlevels:
                        values["email"] = qu.user.email()
                        values["level"] = qu.level
                        if section == "removeuser":
                            values["username"] = qu.user.nickname()
                            #values["owned"] = 0 #TODO: Add owned sections
                            values["verboselevel"] = getLevelName(qu.level).capitalize()
                            values["date"] = str(qu.date)
                    else:
                        errors.append("No rights over user or non-registered user")
                elif section=="newuser":
                    values["backurl"] = "%s/%s" % (adminprefix+release.prefix,section)

                if section == "removeuser":
                    content = getTemplate("removeuser",values)
                else:
                    content = getTemplate("edituser",values)

            elif section in ("images","userfiles","files","removefile"):
                if (user.getFileAdd() and section in ("userfiles","images")) or (user.getFileAdmin() and section=="files"):
                    upp = 10 # Files per page
                    maxpages = 10 # Max pages
                    page = 0 # Current page
                    if context_vars.has_key("subsection") and isReal(context_vars["subsection"]) and context_vars["subsection"]>0:
                        page = int(context_vars["subsection"])-1

                    offset = upp*page
                    nfiles = counter["file"]
                    npages = (nfiles/upp)+((nfiles%upp)>0)
                    if npages == 0:
                        npages = 1

                    pages = []
                    isdialog = context_vars.has_key("isdialog") and context_vars["isdialog"]
                    if isdialog:
                        for i in range(npages):
                            n = i+1
                            pages.append(PageItem(n,str(n),"%s/%s/%d" % (dialogprefix+release.prefix,section,n)))
                    else:
                        for i in range(npages):
                            n = i+1
                            pages.append(PageItem(n,str(n),"%s/%s/%d" % (adminprefix+release.prefix,section,n)))

                    items = []
                    if section == "images":
                        for i in queryAllImageFiles(user,offset,upp):
                            remove = None
                            if not isdialog:
                                remove = adminprefix+release.prefix+fileremoveprefix+i.id
                            items.append(UserImageFileItem(i.id,i.name,remove,formatByteSize(i.size),i.date,Image(imgpreviewprefix+i.id)))
                    else:
                        if section == "userfiles":
                            for i in queryAllFiles(user,offset,upp):
                                remove = adminprefix+release.prefix+fileremoveprefix+i.id
                                items.append(UserFileItem(i.id,i.name,remove,formatByteSize(i.size),i.date))
                        else:
                            for i in queryAllFiles(None,offset,upp):
                                remove = adminprefix+release.prefix+fileremoveprefix+i.id
                                items.append(FileItem(i.id,i.name,remove,formatByteSize(i.size),i.user,i.date))

                    add = ""
                    if user.getFileAdd():
                        add = adminprefix+release.prefix+filenewprefix
                    values = {
                        "page" : page+1,
                        "pagelist" : pages,
                        "items": items,
                        "upp" : upp,
                        "nfiles" : nfiles,
                        "add" : add,
                        "isdialog" : isdialog,
                    }
                    content = getTemplate("filelist",values)
                elif context_vars.has_key("subsection") and section=="removefile":
                    if context_vars.has_key("formsuccess") and context_vars["formsuccess"]:
                        values = {
                            "formsuccess":True,
                            "backurl": adminprefix+release.prefix+"/userfiles"
                            }

                        content = getTemplate("removefile",values)
                    else:
                        subsection = context_vars["subsection"]
                        qu = queryUserFile(subsection)
                        if qu != None and (user.getFileAdmin() or qu.user==user):
                            values = {
                                "form_action": adminprefix+release.prefix+"/%s/%s" % (section,subsection),
                                "id" : qu.id,
                                "filename" : qu.name,
                                "user": qu.user,
                                "date" : qu.date,
                                "backurl": adminprefix+release.prefix+"/userfiles"
                            }
                            content = getTemplate("removefile",values)
                else:
                    errors.append("Access denied")
            elif section == "blogs":
                spp = 10 # Sections per page
                maxpages = 10 # Max pages
                page = 0 # Current page
                if context_vars.has_key("subsection") and isReal(context_vars["subsection"]) and context_vars["subsection"]>0:
                    page = int(context_vars["subsection"])-1

                offset = spp*page
                nsections = sum( counter.getMulti(["%s/blog" % i for i in user.getBlogVisible()]).values() )
                npages = (nsections/spp)+((nsections%spp)>0)
                if npages == 0:
                    npages = 1

                pages = []
                for i in range(npages):
                    n = i+1
                    pages.append(PageItem(n,str(n),"%s%d" % (adminprefix+release.prefix+listprefix,n)))

                sl = queryAllBlogs(offset,spp,user)
                overlevels = user.getBlogVisible()
                items = []
                for i in sl:
                    edit = ""
                    remove = ""
                    if i.level in overlevels or i.author == user.ref:
                        edit = adminprefix+release.prefix+editprefix+i.id
                        remove = adminprefix+release.prefix+removeprefix+i.id
                    items.append(sectionlistItem(i.link,i.id,"%s%s" % (prefix,i.id),edit,remove,i.description,i.parentid,i.author,str(i.lastdate).split(".")[0]))

                add = ""
                if  user.getBlogAdd():
                    add = adminprefix+release.prefix+blognewprefix
                values = {
                    "page" : page+1,
                    "pagelist" : pages,
                    "items": items,
                    "spp" : spp,
                    "nblogs" : nsections,
                    "add" : add
                }
                content = getTemplate("bloglist",values)

            elif section in ("blogadd","blogedit","blogremove"):
                pass

            elif section == "upload":
                if user.getFileAdd():
                    values = context_vars
                    values.update({
                        "form_action": adminprefix+release.prefix+filenewprefix,
                        "form_enctype": "multipart/form-data",
                        "form_id":"upload_noajax_",
                    })
                    if context_vars.has_key("override_form_action"):
                        values["form_action"] = context_vars["override_form_action"]
                    if errors:
                        values["hideform"] = True

                    content = getTemplate("upload",values)
                else:
                    errors.append("Access denied")

            elif section == "users":
                if user.getUserListing():
                    upp = 10 # Users per page
                    maxpages = 10 # Max pages
                    page = 0 # Current page
                    if context_vars.has_key("subsection") and isReal(context_vars["subsection"]) and context_vars["subsection"]>0:
                        page = int(context_vars["subsection"])-1

                    offset = upp*page
                    nusers = counter["user"]
                    npages = (nusers/upp)+((nusers%upp)>0)
                    if npages == 0:
                        npages = 1

                    pages = []
                    for i in range(npages):
                        n = i+1
                        pages.append(PageItem(n,str(n),"%s%d" % (adminprefix+release.prefix+listprefix,n)))

                    sl = queryAllUsers(offset,upp)
                    overlevels = user.getUserEdit()
                    imadmin = user.isadmin()
                    items = []
                    for i in sl:
                        edit = ""
                        remove = ""
                        if i.level in overlevels:
                            edit = adminprefix+release.prefix+usereditprefix+i.user.email()
                            remove = adminprefix+release.prefix+userremoveprefix+i.user.email()
                        items.append(userlistItem(i.user.nickname(),getLevelName(i.level,0),edit,remove,str(i.date).split(".")[0]))

                    add = ""
                    if user.getUserAdd():
                        add = adminprefix+release.prefix+usernewprefix
                    values = {
                        "page" : page+1,
                        "pagelist" : pages,
                        "items": items,
                        "upp" : upp,
                        "nusers" : nusers,
                        "add" : add
                    }
                    content = getTemplate("userlist",values)
                    #content = db.GqlQuery("SELECT * FROM UserModel").count()
                else:
                    errors.append("Access denied")

            elif section == "counters":
                if user.isadmin():
                    levels = user.getBlogVisible()
                    ks = "%s/section"
                    kb = "%s/blog"
                    counters = Glass( counter.getMulti([ks % i for i in levels]+[kb % i for i in levels]) )
                    cl = [Glass({
                                "name":getLevelName(i),
                                "level":i,
                                "items":(
                                    Glass({
                                        "type": "section",
                                        "name": ks % i,
                                        "value": counters[ks % i] or 0,
                                        "of": countSectionsByVisibility(i) or 0,
                                        }),
                                    Glass({
                                        "type": "blog",
                                        "name": kb % i,
                                        "value": counters[kb % i] or 0,
                                        "of": countBlogsByVisibility(i) or 0,
                                        }),
                                    ),
                                }) for i in levels]
                    values = {
                        "form_action": adminprefix+release.prefix+"/counters",
                        "counters" : cl
                        }
                    values.update(context_vars)
                    content = getTemplate("fixpages",values)
                else:
                    errors.append("Access denied")
            elif section == "maintenance":
                if user.isadmin():
                    values = {
                        "form_action": adminprefix+release.prefix+"/maintenance",
                        }
                    values.update(context_vars)
                    content = getTemplate("maintenance",values)
                else:
                    errors.append("Access denied")

            elif section == defaultAdminSection:
                log=""
                debug = ""
                req = []
                res = []
                if user.isadmin():
                    ms = memcache.get('DB_TMP_STATS')
                    if ms != None:
                        for i, j in sorted(ms.items(), key=operator.itemgetter(0)):
                            log+='%s : %s <br/>' % (i, j)
                        log += "Cached menuitems: "
                        vcache = varCache["menuitems"]
                        if vcache == None:
                            log += "No data."
                        else:
                            for i in vcache.keys():
                                log += "%s " % i
                    resindx = {}
                    for i,j in context_vars["response"].headers.items():
                        if resindx.has_key(i):
                            res[ resindx[i] ].value.append(j)
                        else:
                            resindx[i] = len(res)
                            res.append( Glass({"name":i,"value":[j]}) )
                    req = [ Glass({"name":i,"value":j}) for i, j in context_vars["request"].headers.items() ]

                values = {
                    "name" : APPCONFIG["name"],
                    "app" : APPCONFIG["app"],
                    "version" : APPCONFIG["version"],
                    "log" : log,
                    "server_management" : user.getServerAdmin(),
                    "debug" : debug,
                    "req" : req,
                    "res" : res
                }
                 # Sección por defecto
                content = getTemplate("admin",values)

        self.setVars(context_vars, user, linkitems, menuitems, sideitems, prefix, content, section, errors, True)

class generateDialog(generateAdminSection):
    def __init__(self,context_vars=None):
        self.errors = []
        if context_vars==None:
            context_vars = {}

        if context_vars.has_key("section"):
            section = context_vars["section"]
        else:
            section = None

        release = getRelease(context_vars)
        context_vars["release"] = release

        context_vars["isdialog"] = True
        context_vars["skip_menus"] = True
        if section in APPCONFIG["dialogable"]:
            context_vars["override_form_action"]=dialogprefix+release.prefix+"/"+section
            generateAdminSection.__init__(self, context_vars)
        else:
            self.content = ""

    def getMain(self):
        return tagStrip(getTemplate("dialog",{"content": self.content,"errors":self.errors}))
