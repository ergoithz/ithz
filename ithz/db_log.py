# Copyright 2008 Jens Scheffler
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


from google.appengine.api import apiproxy_stub_map
from google.appengine.api import memcache
from google.appengine.datastore import datastore_index
import logging
import operator


def db_log(model, call, details=''):
  """Call this method whenever the database is invoked.
  
  Args:
    model: the model name (aka kind) that the operation is on
    call: the kind of operation (Get/Put/...)
    details: any text that should be added to the detailed log entry.
  """
  
  # First, let's update memcache
  if model:
    stats = memcache.get('DB_TMP_STATS')
    if stats is None: stats = {}
    key = '%s_%s' % (call, model)
    stats[key] = stats.get(key, 0) + 1
    memcache.set('DB_TMP_STATS', stats)
  
  # Next, let's log for some more detailed analysis
  logging.debug('DB_LOG: %s @ %s (%s)', call, model, details)


def patch_appengine():
  """Apply a hook to app engine that logs db statistics."""
  def model_name_from_key(key):
    return key.path().element_list()[0].type()
    
  def hook(service, call, request, response):
    assert service == 'datastore_v3'
    if call == 'Put':
      for entity in request.entity_list():
        db_log(model_name_from_key(entity.key()), call)
    elif call in ('Get', 'Delete'):
      for key in request.key_list():
        db_log(model_name_from_key(key), call)
    elif call == 'RunQuery':
      kind = datastore_index.CompositeIndexForQuery(request)[1]
      db_log(kind, call)
    else:
      db_log(None, call)
      
  apiproxy_stub_map.apiproxy.GetPreCallHooks().Append(
      'db_log', hook, 'datastore_v3')


def main():
  """A very simple handler that will print the temporary statistics."""
  print 'Content-Type: text/plain'
  print ''
  print 'Mini stats'
  print '----------'
  stats = memcache.get('DB_TMP_STATS')
  if stats is None: stats = {}
  for name, count in sorted(stats.items(), key=operator.itemgetter(0)):
    print '%s : %s' % (name, count)
  print '----------'

  
if __name__ == "__main__":
  main()
