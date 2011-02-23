import cPickle as pickle

from sqlalchemy.engine.reflection import Inspector

from model import *
from storage import *

eids = pickle.load(open("eids.txt"))
insp = Inspector.from_engine(db)

s = Storage("uoit")

for table in metadata.sorted_tables:
  pk = [col.name for col in table.columns if col.primary_key][0]

  for row in db.execute(table.select()):
    eid = eids[(unicode(row[pk]), table.name)]

    for fk in insp.get_foreign_keys(table.name):
      id = fk["constrained_columns"][0]
      type = fk["referred_table"]

      s.add_link(eid, eids[(unicode(row[id]), type)], type)
