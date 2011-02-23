from model import *
from storage import *

with Storage("uoit") as s:
  for table in metadata.sorted_tables:
    t_name = table.name
    pk_col = [col for col in table.columns if col.primary_key][0]

    for row in db.execute(select([table])):
      pk_name = pk_col.name
      pk_val = unicode(row[pk_col.name])
      eid = "%s%s%s" % (pk_name, pk_val.replace(" ", "_"), t_name)
      entity = { "eid": eid }

      for column in table.columns:
        entity[column.name] = row[column.name]

        s.add_data({
          "id": pk_val,
          "eid": eid,
          "type": t_name,
          "value": unicode(row[column.name])
        })

      s.add_entity(entity)
