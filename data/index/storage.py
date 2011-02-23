import pickle
import shelve

from shutil import rmtree

import xapian as xap

class Storage:
  def __init__(self, dbname):
    self.data_db = self._create_db(dbname, "data")
    self.link_db = self._create_db(dbname, "link")

    self.indexer = xap.TermGenerator()
    self.indexer.set_stemmer(xap.Stem("none"))

    self.entities = shelve.open("entities.db", "c")
    self.eid_cache = {}

  def __enter__(self):
    return self

  def add_data(self, data):
    """
    Expects a hash in the following format:
    eid:  unique eid
    type:  type of entity
    value:  text to index
    """
    doc = self._create_doc(data["value"])
    eid = data["eid"]
    type = data["type"]

    # Add additional properties to doc.
    doc.add_value(0, eid)
    doc.add_value(1, type)

    # Cache EID.
    self.eid_cache[(data["id"], type)] = eid
    self.data_db.add_document(doc)

  def add_link(self, e1, e2, type):
    doc = self._create_doc(e2)
    doc.add_term("I%s" % e1, 1)
    doc.add_term("T%s" % type, 1)
    doc.add_value(0, e1)

    self.link_db.add_document(doc)

  def add_entity(self, h):
    self.entities[str(h["eid"])] = h

  def get_entity(self, eid):
    return self.entities[eid]

  def _create_db(self, name, type):
    return xap.WritableDatabase("%s_%s.idx" % (name, type),
      xap.DB_CREATE_OR_OPEN)

  def _create_doc(self, text):
    doc = xap.Document()
    doc.set_data(text)

    self.indexer.set_document(doc)
    self.indexer.index_text(text)

    return doc

  def __exit__(self, exc_type, exc_value, traceback):
    with open("eids.txt", "w") as f:
      pickle.dump(self.eid_cache, f) # was json.dump()

    self.entities.close()
