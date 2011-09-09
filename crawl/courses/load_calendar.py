from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import *
from time import time
from optparse import OptionParser
import sys
from subprocess import Popen, PIPE
import re

def get_course_descriptions(pdf):
  p = Popen(['pdftotext', '-raw', '-enc', 'ASCII7', '-q', '-nopgbrk', pdf, '-'], stdout=PIPE)
  section_pattern = re.compile(r"^(UNDER)?GRADUATE COURSE DESCRIPTIONS$")
  end_pattern = re.compile(r'^INDEX$')
  entry_pattern = re.compile(r"^[A-Z]{4} [0-9]{4}. [A-Z]+")
  ignore_patterns = [re.compile(r'^section\s*\d+:'), re.compile('^\d+$')]
  sentence_pattern = re.compile(r"(^\s*$)|(.*\.)|(.*\s+)")
  in_section = False
  buf = []
  for line in (x.strip() for x in p.stdout.xreadlines()):
    if end_pattern.search(line):
      break
    # Skip the top portion
    if not in_section:
      if section_pattern.search(line):
        in_section = True
    else:
      if (not line) or any(x.search(line) for x in ignore_patterns):
        continue
      if entry_pattern.search(line) and ((not buf) or buf[-1][-1] in "."):
        if buf:
          yield " ".join(buf)
        buf = [line]
      else:
        if buf: buf.append(line)

Base = declarative_base()

class CalendarEntry(Base):
  __tablename__ = "calendar"
  code = Column(String, primary_key=True)
  title = Column(String(200))
  description = Column(String(255))
  prerequisite = Column(String(100))

  def parse(self, desc):
    self.code = desc[:10].strip().lower()
    try:
      (body, self.prerequisite)  = re.split(r"\s+Prerequisites:\s+", desc[10:], maxsplit=1)
    except ValueError, e:
      (body, self.prerequisite) = desc[10:], None
    (self.title, self.description) = body.split(".", 1)
    return self

if __name__ == '__main__':

  parser = OptionParser()
  parser.add_option("--url", dest="url", help="""
  e.g.:
    --url postgres://<user>:<password>@localhost/<dbname>
    --url sqlite:///<filename>
  """)
  parser.add_option("--pdf", dest="pdf", help="source of the pdf")
  (opt, args) = parser.parse_args()

  if opt.pdf:
    pdf = opt.pdf
  elif args:
    pdf = args[0]
  else:
    parser.print_help()
    sys.exit(0)

  if not opt.url:
    parser.print_help()
    sys.exit(0)

  engn = create_engine(opt.url)
  Base.metadata.create_all(engn)
  Session = sessionmaker()
  Session.configure(bind = engn)
  session = Session()
  s = time()
  i = 0
  errors = []
  for (i, line) in enumerate(get_course_descriptions(pdf)):
    c = CalendarEntry().parse(line)
    try:
      session.add(c)
      session.commit()
    except Exception, e:
      errors.append(c)
      session.rollback()
    if i and i % 100 == 0:
      print "[%.4d] processed" % (i)
  print "Processed %d entries in %.2f seconds" % (i, time()-s)
  print "There are %d errors including these courses" % len(errors)
  print "\n".join("%s: %s" % (c.code, c.title) for c in errors)
