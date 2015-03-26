#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#



import md5
import os

import django

import django.conf
django.conf.settings.configure(
    DEBUG=False,
    TEMPLATE_DEBUG=False,
    TEMPLATE_LOADERS=(
      'django.template.loaders.filesystem.load_template_source',
    ),
)

import django.template
import django.template.loader
from google.appengine.ext import webapp

'''
#{% rename object.get_relatedObject_list relatedObject_list %}
register = django.template.Library()

class RenameNode( django.template.Node ):
    def __init__( self, fromvar, tovar ):
        self.fromvar = fromvar
        self.tovar = tovar

    def render( self, context ):
        context[self.tovar] = Template.resolve_variable( self.fromvar, context )
        # very important: don't forget to return a string!!
        return ''

@register.tag
def rename( parser, token ):
    tokens = token.contents.split()
    if len( tokens ) != 3:
        raise django.template.TemplateSyntaxError, \
            "'%s' tag takes two arguments" % tokens[0]
    return RenameNode( tokens[1], tokens[2] )
'''

def render(template_path, template_dict, debug=False):
  t = load(template_path, debug)
  return t.render(Context(template_dict))


template_cache = {}
def load(path, debug=False):
  abspath = os.path.abspath(path)

  if not debug:
    template = template_cache.get(abspath, None)
  else:
    template = None

  if not template:
    directory, file_name = os.path.split(abspath)
    new_settings = {
        'TEMPLATE_DIRS': (directory,),
        'TEMPLATE_DEBUG': debug,
        'DEBUG': debug,
        }
    old_settings = _swap_settings(new_settings)
    try:
      template = django.template.loader.get_template(file_name)
    finally:
      _swap_settings(old_settings)

    if not debug:
      template_cache[abspath] = template

    def wrap_render(context, orig_render=template.render):
      URLNode = django.template.defaulttags.URLNode
      save_urlnode_render = URLNode.render
      old_settings = _swap_settings(new_settings)
      try:
        URLNode.render = _urlnode_render_replacement
        return orig_render(context)
      finally:
        _swap_settings(old_settings)
        URLNode.render = save_urlnode_render

    template.render = wrap_render

  return template


def _swap_settings(new):
  settings = django.conf.settings
  old = {}
  for key, value in new.iteritems():
    old[key] = getattr(settings, key, None)
    setattr(settings, key, value)
  return old


def create_template_register():
    return django.template.Library()


def register_template_library(package_name):
  if not django.template.libraries.get(package_name, None):
    django.template.add_to_builtins(package_name)


Template = django.template.Template
Context = django.template.Context

def _urlnode_render_replacement(self, context):
  args = [arg.resolve(context) for arg in self.args]
  try:
    app = webapp.WSGIApplication.active_instance
    handler = app.get_registered_handler_by_name(self.view_name)
    return handler.get_url(implicit_args=True, *args)
  except webapp.NoUrlFoundError:
    return ''
