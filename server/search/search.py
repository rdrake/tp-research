import shelve
import sys

import xapian as xap

class Search(object):
  def __init__(self, path):
    self.path = path
    self.db = xap.Database(path)

    self.enquire = xap.Enquire(self.db)
    self.qp = xap.QueryParser()

    #self.qp.set_default_op(xap.Query.OP_AND)

    self.qp.set_stemmer(xap.Stem("none"))
    self.qp.set_database(self.db)
    self.qp.set_stemming_strategy(xap.QueryParser.STEM_NONE)

  def _search(self, qs, k):
    query = self.qp.parse_query(qs)
    self.enquire.set_query(query)

    return self.enquire.get_mset(0, k)

class DataSearch(Search):
  def __init__(self, dbname):
    Search.__init__(self, "..\\prepare\\%s_data.idx" % dbname)

  def search(self, qs, k=10):
    return self._search(qs, k)

class LinkSearch(Search):
  def __init__(self, dbname):
    Search.__init__(self, "..\\prepare\\%s_link.idx" % dbname)

    self.qp.add_boolean_prefix("eid", "I")
    self.qp.add_boolean_prefix("type", "T")

    self.enquire.set_weighting_scheme(xap.BoolWeight())

  def get_references(self, eid, T=None, k=10):
    q = "eid:%s" % eid

    if T:
      q += " type:%s" % T

    return self._search(q, k)

  def get_links(self, eid, T=None, k=10):
    q = eid

    if T:
      q += " type:%s" % T

    return self._search(q, k)

class EntitySearch(Search):
  def __init__(self):
    self.entities = shelve.open("..\\prepare\\entities.db")

  def get(self, eid):
    return self.entities.get(eid)
