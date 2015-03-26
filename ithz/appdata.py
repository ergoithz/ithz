# -*- coding: utf-8 -*-,
import ithz.mimetypes as mime
from ithz.utils import u
from os import getcwd, sep, environ

class __Release(object):
    def __init__(self,name,code,prefix,ref,desc=None,browser=None,message_dict=None):
        self.name = name
        self.code = code
        self.prefix = prefix
        self.str = message_dict
        self.ref = ref
        
        if desc == None:
            self.description = self.name.capitalize()
        else:
            self.description = desc
        
        if browser == None:
            self.browser = ()
        else:
            self.browser = browser

class __Message_dict(object):
    def __init__(self,dict=None):
        if dict is None:
            dict = {}
        self.dict = dict
        
    def __getattribute__(self,id):
        if id=="dict":
            return object.__getattribute__(self, id)
        else:
            return u(self.dict[id])
            
def __getServerId():
    if environ.get('SERVER_SOFTWARE','').startswith('Devel'):
        return "local"
    try:
        fd   = open('/base/python_dist/search.config')
        data = fd.read()
        fd.close()
    except IOError:
        return 'unknown'
    
    return '%s' % data.__hash__()

__langs = {
    "es":__Message_dict(
            {
                "rss_orig_error":"El origen de datos por sindicación RSS aún no ha sido procesado. Por favor, inténtelo más tarde.",
                "e404":"La página no existe.",
            }),
    "en":__Message_dict(
            {
                "rss_orig_error":"The rss feed has been not proccessed yet.",
                "e404":"Page not found",
            }),
    }
__av = getcwd().split(sep)[-2:]
APPCONFIG = {
    "name" : "ithz CMS",
    "version" : __av[1],
    "app" : __av[0],
    "license" : "GPLv3",
    "server" : __getServerId(),
    "releases" : [
        __Release("english","en_GB","en","en","English site",("en-US","en"),__langs["es"]),
        __Release("español","es_ES","es","es","Versión en español",("es-ES","es"),__langs["es"]),
        ],
    "releases_by_prefix" : {},
    "releases_by_language" : {},
    "prefixes" : [],
    "image_mimes" : mime.jpg + mime.png + mime.gif + mime.svg,
    "gae_image_mimes" : mime.jpg + mime.png + mime.gif + mime.bmp + mime.tiff + mime.ico,
    "dialogable": ("upload","images"),
    }

for i in APPCONFIG["releases"]:
    for j in i.browser:
        APPCONFIG["releases_by_language"][j] = i
    APPCONFIG["releases_by_prefix"][i.prefix] = i
    APPCONFIG["prefixes"].append(i.prefix)
