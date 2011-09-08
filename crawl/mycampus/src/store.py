from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import *
import sys
import json
import re
from datetime import datetime
from time import time
from optparse import OptionParser

parser = OptionParser()
parser.add_option("--url", dest='url', help="""
e.g.:
  --url postgres://<user>:<password>@localhost/<dbname>
  --url sqlite:///<filename>
""")

(opt, args) = parser.parse_args()

if not (args or opt.url):
  parser.print_help()
  sys.exit()

print "url=%s" % opt.url

engn = create_engine(opt.url)

Base = declarative_base()

class Course(Base):
  __tablename__ = 'courses'

  code = Column(String, primary_key=True)
  title = Column(String)

class Section(Base):

  __tablename__ = 'sections'

  id = Column(Integer, primary_key=True)
  actual = Column(Integer)
  campus = Column(String)
  capacity = Column(Integer)
  credits = Column(Float)
  levels = Column(String)
  registration_start = Column(Date)
  registration_end = Column(Date)
  semester = Column(String)
  sec_code = Column(String)
  sec_number = Column(String)
  year = Column(String)
  course = Column(String, ForeignKey('courses.code'))

class Instructor(Base):

  __tablename__ = 'instructors'

  id = Column(Integer, primary_key=True)
  name = Column(String)

class Schedule(Base):

  __tablename__ = 'schedules'

  id = Column(Integer, primary_key=True)
  date_start = Column(Date)
  date_end = Column(Date)
  day = Column(String)
  schedtype = Column(String)
  hour_start = Column(Integer)
  hour_end = Column(Integer)
  min_start = Column(Integer)
  min_end = Column(Integer)
  classtype = Column(String)
  location = Column(String)
  section_id = Column(Integer, ForeignKey('sections.id'))

class Teaches(Base):
  __tablename__ = 'teaches'
  id = Column(Integer, primary_key=True)
  schedule_id = Column(Integer, ForeignKey('schedules.id'))
  instructor_id = Column(Integer, ForeignKey('instructors.id'))
  position = Column(String)

Base.metadata.create_all(engn)

Session = sessionmaker()
Session.configure(bind = engn)

def sections():
  for line in sys.stdin.xreadlines:
    yield json.loads(line)

re_title = re.compile(r'(.*) - (\d{5}) - (\w+ \w+) - (\w+)')
def parse_title(line):
  """
  Blah blah - 75693 - CSCI 3030U - 007
  """
  (title, sec_code, code, sec_num) = re_title.findall(line)[0]
  return (code, title, sec_code, sec_num)

def parse_credits(line):
  """
             3.000 credits
  """
  if line:
    return float(line[:-8])
  else:
    return None

def parse_daterange(line):
  """
  jun 28, 2010 to jan 21, 2011
  or
  jan 20, 2011 - apr 14, 2011
  """

  if ' to ' in line:
    return map(
      lambda x: datetime.strptime(x, "%b %d, %Y") \
      if x else None,
               line.split(" to "))
  else:
    return map(
      lambda x: datetime.strptime(x, "%b %d, %Y") \
      if x else None,
               line.split(" - "))

def parse_timerange(line):
  """ 3:40 pm - 5:00 pm 
  or TBA
  """
  if not line or not line.strip() or 'TBA' in line: 
    return None, None, None, None
  
  start, end = map(
        lambda x: datetime.strptime(x, "%I:%M %p"),
        line.strip().split(' - '))

  return start.hour, start.minute, end.hour, end.minute

def parse_semester(line):
  """
  uoit winter 2011
  """
  return (line, line[-4:])

def store_section(sql, section_js, i):
  (code, title, sec_code, sec_num) = parse_title(section_js['title'])
  course = Course()
  course.code = code
  course.title = title

  sec = Section()
  sec.actual = int(section_js['actual'])
  sec.campus = section_js['campus']
  sec.capacity = int(section_js['capacity'])
  sec.credits = parse_credits(section_js.get('credits'))
  sec.levels = section_js['levels']
  sec.registration_start, sec.registration_end = parse_daterange(
    section_js['registration'])
  sec.semester, sec.year = parse_semester(section_js['semester'])

  sec.course = course.code
  sec.sec_code = sec_code
  sec.sec_number = sec_num

  if sql.query(Course).filter(Course.code == course.code).count() == 0:
    sql.add(course)

  sql.add(sec)

  if section_js.get('schedule_list'):
    for sch_js in section_js.get('schedule_list'):
      sch = Schedule()
      sch.date_start, sch.date_end = parse_daterange(sch_js['daterange'])
      sch.day = sch_js['days']
      sch.schedtype = sch_js['scheduletype']
      sch.hour_start, sch.min_start, \
      sch.hour_end, sch.min_end = parse_timerange(sch_js['time'])
      sch.classtype = sch_js['type']
      sch.location = sch_js.get('where')
      sch.section_id = sec.id
      sql.add(sch)
      for inst_js in sch_js.get('instructor_list', []):
        name = inst_js.get('name')
        position = inst_js.get('position')
        if name and not 'TBA' in name:
          q = sql.query(Instructor).filter(Instructor.name == name).all()
          if not q:
            instructor = Instructor()
            instructor.name = name
            sql.add(instructor)
          else:
            instructor = q[0]
          teaches = Teaches()
          teaches.instructor_id = instructor.id
          teaches.schedule_id = sch.id
          sql.add(teaches)
  
def load(session, lines):
  print >>sys.stderr, "Loading database..."
  s = time()
  for (i, line) in enumerate(lines):
    sec_js = json.loads(line)
    store_section(session, sec_js, i)
    if i and i % 100 == 0:
      session.commit()
  session.commit()
  print >>sys.stderr, "loaded %d sections in %.2f seconds" % (i, time()-s)

if __name__ == '__main__':
  session = Session()
  lines = sys.stdin.xreadlines()
  load(session, lines)
