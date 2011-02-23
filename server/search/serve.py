import json
import os
import sys

from twisted.internet import defer, reactor, threads
from twisted.python import log
from twisted.web import http, server, static, resource

from search import *

log.startLogging(sys.stdout)

TOP_K_LINKS = 100000

# Shamelessly "adapted" from SO:
# http://stackoverflow.com/questions/455580/json-datetime-between-python-and-javascript
def handler(obj):
  """
  Handles convert Python datetime.date -> JS-friendly dates.
  """
  if hasattr(obj, "isoformat"):
    return obj.isoformat()

  return obj

class CommonResource(resource.Resource):
  def __init__(self):
    resource.Resource.__init__(self)

  def _doWork(self, args):
    pass

  def _pfunc(self, m):
    return m.document.get_value(0)

  def search(self, s_func, *args, **kwargs):
    if len(args) == 0 or args[0] is None:
      return []

    q = " ".join(args[0])

    return [self._pfunc(match) for match in s_func(q, *args[1:], **kwargs)]

  def _doneWork(self, value, request):
    if value is not None:
      request.setHeader("Content-Type", "application/json")
      request.write(json.dumps({ "data": value }, default=handler))

    request.finish()

  def render_GET(self, request):
    d = threads.deferToThread(self._doWork, request.args)
    request.notifyFinish().addErrback(self._cancel, d)
    d.addCallback(self._doneWork, request)

    return server.NOT_DONE_YET

  def _cancel(self, err, deferred):
    deferred.cancel()

class EntityResource(CommonResource):
  isLeaf = True

  def __init__(self):
    CommonResource.__init__(self)
    self.dp = EntitySearch()

  def _doWork(self, args):
    if len(args) == 0:
      return {}

    return self.dp.get(args["eid"][0])

class SearchResource(CommonResource):
  isLeaf = True

  def __init__(self):
    self.dp = DataSearch("uoit")
    self.extra_dp = EntitySearch()

  def _doWork(self, args):
    if "q" not in args:
      return None

    results = self.search(self.dp.search, args["q"])

    if "expand" in args:
      return [self.extra_dp.get(result) for result in results]

    return results

class LinkResource(CommonResource):
  def __init__(self):
    CommonResource.__init__(self)
    self.dp = LinkSearch("uoit")
    self.extra_dp = EntitySearch()

  def _doWork(self, args):
    """
    CLEAN ME UP!
    """
    t = None
    res = None

    if "type" in args:
      t = args["type"][0]

    if t:
      res = self.search(self.func, args["eid"], T=t, k=TOP_K_LINKS)
    else:
      res = self.search(self.func, args["eid"], k=TOP_K_LINKS)

    if "expand" in args:
      return [self.extra_dp.get(result) for result in res]

    return res

class ReferencedResource(LinkResource):
  """
  Search for an entity ID which will return the referencing EID.
  """
  isLeaf = True

  def __init__(self):
    LinkResource.__init__(self)
    self.func = self.dp.get_references

  def _pfunc(self, m):
    return m.document.get_data()

class ReferencesResource(LinkResource):
  """
  Search for eid:<eid> which sends back all entities referenced by the search
  entity ID.
  """
  isLeaf = True

  def __init__(self):
    LinkResource.__init__(self)
    self.func = self.dp.get_links

root = static.File(os.getcwd())
link = LinkResource()

link.putChild("to", ReferencedResource())
link.putChild("from", ReferencesResource())

root.putChild("entity", EntityResource())
root.putChild("search", SearchResource())
root.putChild("links", link)

reactor.listenTCP(8080, server.Site(root))
reactor.run()
