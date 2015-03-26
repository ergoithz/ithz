# -*- coding: utf-8 -*-
import sys
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import webapp

import ithz.utils
import ithz.security
import ithz.presentation
import ithz.forms
import ithz.files
import ithz.cron
import ithz.appdata

sys.modules['__main__'] = sys.modules[__name__]

# RequestHandlers
class Section(webapp.RequestHandler):
    def get(self,prefix=None,section=None,contexto=None):
        if prefix=="/":
            prefix=None

        if contexto==None:
            contexto = {}

        if not contexto.has_key("user"):
            contexto["user"] = ithz.security.User()

        if not contexto.has_key("chronos"):
            contexto["chronos"] = ithz.utils.XTimer()

        contexto["prefix"] = prefix
        contexto["section"] = section
        self.response.out.write(ithz.presentation.generateSection(contexto).getMain())

class AJAXSection(Section):
    def get(self,prefix=None,section=None,contexto=None):

        if contexto==None:
            contexto = {}

        if not contexto.has_key("user"):
            contexto["user"] = ithz.security.User()

        if not contexto.has_key("chronos"):
            contexto["chronos"] = ithz.utils.XTimer()

        contexto["prefix"] = prefix
        contexto["section"] = section
        info = ithz.presentation.generateSection(contexto)

        self.response.headers["Content-Type"] = "text/javascript; charset=utf-8"
        self.response.out.write(info.getAjax())

class AdminSection(webapp.RequestHandler):
    def get(self,prefix=None,section=None,arg=None,contexto=None):
        if contexto==None:
            contexto = {}

        if arg!=None:
            contexto["subsection"] = arg

        if not contexto.has_key("user"):
            contexto["user"] = ithz.security.User()

        if not contexto.has_key("chronos"):
            contexto["chronos"] = ithz.utils.XTimer()

        contexto["prefix"] = prefix
        contexto["section"] = section
        contexto["request"] = self.request
        contexto["response"] = self.response
        self.response.out.write(ithz.presentation.generateAdminSection(context_vars=contexto).getMain())

    def post(self,prefix=None,section=None,arg=None):
        if section==None:
            self.redirect("/");
            return

        chronos = ithz.utils.XTimer()
        results = ithz.forms.Post(self.request,section,arg)
        results.contexto["chronos"] = chronos
        results.contexto["prefix"] = prefix
        self.get(prefix,results.section,arg=results.arg,contexto=results.contexto)

class AJAXAdminSection(AdminSection):
    def get(self,prefix=None,section=None,arg=None,contexto=None):
        if contexto==None:
            contexto = {}

        if arg!=None:
            contexto["subsection"] = arg

        if not contexto.has_key("user"):
            contexto["user"] = ithz.security.User()

        if not contexto.has_key("chronos"):
            contexto["chronos"] = ithz.utils.XTimer()

        contexto["prefix"] = prefix
        contexto["section"] = section
        contexto["request"] = self.request
        contexto["response"] = self.response
        info = ithz.presentation.generateAdminSection(contexto)
        self.response.headers["Content-Type"] = "text/javascript; charset=utf-8"
        self.response.out.write(info.getAjax())

    def post(self,prefix=None,section=None,arg=None):
        if section==None:
            self.redirect("/");
            return

        chronos = ithz.utils.XTimer()
        results = ithz.forms.Post(self.request,section,arg)
        results.contexto["prefix"] = prefix
        results.contexto["chronos"] = chronos
        self.get(prefix,results.section,arg=results.arg,contexto=results.contexto)

class Dialog(webapp.RequestHandler):
    def get(self,prefix=None,section=None,arg=None,contexto=None):
        if contexto==None:
            contexto = {}
        if prefix != None:
            if prefix not in ithz.appdata.APPCONFIG["releases_by_prefix"]:
                arg = section
                section = prefix
                release = None
            else:
                contexto["prefix"] = prefix

        if not contexto.has_key("user"):
            contexto["user"] = ithz.security.User()
        if not contexto.has_key("chronos"):
            contexto["chronos"] = ithz.utils.XTimer()
        if arg!=None:
            contexto["subsection"] = arg

        contexto["section"] = section
        contexto["request"] = self.request
        contexto["response"] = self.response
        dialog = ithz.presentation.generateDialog(contexto)
        self.response.out.write(dialog.getMain())

    def post(self,prefix=None,section=None,arg=None):
        if section==None:
            self.redirect("/");
            return
        chronos = ithz.utils.XTimer()
        results = ithz.forms.DialogPost(self.request,section,arg)
        results.contexto["chronos"] = chronos
        if prefix != None:
            results.contexto["prefix"] = prefix
        self.get(prefix,results.section,arg=results.arg,contexto=results.contexto)

class File(webapp.RequestHandler):
    def get(self,id=None):
        if "/" in id:
            id = id.split("/")[0]
        r = ithz.files.generateFile(id)
        if r.success:
            self.response.headers["Content-Type"] = r.mime
            self.response.out.write(r.content)
        else:
            self.error(404)

class ImageFile(webapp.RequestHandler):
    def get(self,id=None):
        if "/" in id:
            id = id.split("/")[0]
        r = ithz.files.generateImageFile(id)
        if r.success:
            if r.content:
                self.response.headers["Content-Type"] = r.mime
                self.response.out.write(r.content)
            else:
                try:
                    self.response.headers["Content-Type"] = "image/png"
                    f = open("static/imgs/image.png")
                    content = f.read()
                    f.close()
                    self.response.out.write(content)
                except IOError:
                    self.error(500)
        else:
            self.error(404)

class CronJobs(webapp.RequestHandler):
    def get(self,id=None):
        user = ithz.security.User()
        if user.isadmin():
            ithz.cron.do(id)
        else:
            self.error(404)

application = webapp.WSGIApplication(
    [
     ('/cron/(.*)',CronJobs),
     ('/admin',AdminSection),
     ('/ajax/admin',AJAXAdminSection),
     (r'/admin/(.*)/(.*)/(.*)',AdminSection),
     (r'/admin/(.*)/(.*)',AdminSection),
     (r'/admin/(.*)',AdminSection),
     (r'/ajax/admin/(.*)/(.*)/(.*)',AJAXAdminSection),
     (r'/ajax/admin/(.*)/(.*)',AJAXAdminSection),
     (r'/ajax/admin/(.*)',AJAXAdminSection),
     (r'/ajax/(.*)/(.*)',AJAXSection),
     (r'/ajax/(.*)',AJAXSection),
     (r'/file/(.*)',File),
     (r'/preview/(.*)',ImageFile),
     (r'/dialog/(.*)/(.*)/(.*)',Dialog),
     (r'/dialog/(.*)/(.*)',Dialog),
     (r'/dialog/(.*)',Dialog),
     (r'/(.*)/(.*)',Section),
     (r'/(.*)', Section),
     (r'(.*)', Section),
    ],
    debug=True)
