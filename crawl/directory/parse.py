import json

# "iglob" sounds dumb.
from glob import iglob as glob
from os import path

### PyParsing-related things ###
from pyparsing import *

(tr_start, tr_end) = map(Suppress, makeHTMLTags("TR"))
(td_start, td_end) = map(Suppress, makeHTMLTags("TD"))
(a_start, a_end) = map(Suppress, makeHTMLTags("A"))

# Grab rows of tables.
row = tr_start + \
  td_start + \
    Word(alphas + "-").setResultsName("type") + Optional(":").suppress() + \
  td_end + \
  td_start + \
    Optional(a_start) + CharsNotIn("<").setResultsName("value") + Optional(a_end) + \
  td_end + \
tr_end
### All done, go on now ###

BASE_PATH = "pages"

def get_file_paths():
  return glob(path.join(BASE_PATH, "*.html"))

def parse_file(file_path):
  # Easiest just to parse a single line.
  data = " ".join([x.strip() for x in open(file_path).readlines()])

  for (d, s_loc, e_loc) in row.scanString(data):
    yield(( d.type, d.value ))

if __name__ == "__main__":
  directory = []

  for file_path in get_file_paths():
    info = {}

    for parsed_info in parse_file(file_path):
      info[parsed_info[0]] = parsed_info[1]

    directory.append(info)

json.dump({ "directory": directory }, open("directory.json", "w"))
