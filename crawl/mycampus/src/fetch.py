import urllib2
import urllib
import re


SITE = "http://ssbprod1.aac.mycampus.ca"
URL_TERMS = "/pls/prod/bwckschd.p_disp_dyn_sched?TRM=U"
EXTRACT_TERM = re.compile(r'<OPTION VALUE="(\d+)\">')
EXTRACT_SUBJ = re.compile(r'<OPTION VALUE="([A-Z]+)\">')

def fetch(url, data=None, header=None):
  if not url.startswith("http"):
    url = SITE + url
  req = urllib2.Request(url)

  if data:
    req.add_data(urllib.urlencode(data))

  if header:
    [req.add_header(*x) for x in header.items()]

  resp = urllib2.urlopen(req)
  html = resp.read()

  return html

def fetch_terms ():
  html = fetch(URL_TERMS)
  for line in html.split("\n"):
    _ = EXTRACT_TERM.findall(line)
    if _:
      yield _[0]

def fetch_subjects(term):
  url = '/pls/prod/bwckgens.p_proc_term_date'
  data = dict(p_calling_proc="bwckschd.p_disp_dyn_sched",
              TRM="U",
              p_term=term)
  html = fetch(url, data)
  for line in html.split('\n'):
    _ = EXTRACT_SUBJ.findall(line)
    if _:
      yield _[0]

def fetch_myc(term, subjects):
  url = "/pls/prod/bwckschd.p_get_crse_unsec"
  data = [
      ("TRM", "U"),
      ("term_in", term),
      ("sel_subj", "dummy"),
      ("sel_day", "dummy"),
      ("sel_schd", "dummy"),
      ("sel_insm", "dummy"),
      ("sel_camp", "dummy"),
      ("sel_levl", "dummy"),
      ("sel_sess", "dummy"),
      ("sel_instr", "dummy"),
      ("sel_ptrm", "dummy"),
      ("sel_attr", "dummy"),
      ("sel_crse", ""),
      ("sel_title", ""),
      ("sel_from_cred", ""),
      ("sel_to_cred", ""),
      ("begin_hh", "0"),
      ("begin_mi", "0"),
      ("begin_ap", "a"),
      ("end_hh", "0"),
      ("end_mi", "0"),
      ("end_ap","a"),
      ("sel_subj", "dummy")
  ] + [ ('sel_subj', x) for x in subjects ]

  return fetch(url, data)

if __name__ == '__main__':
  from optparse import OptionParser
  import sys
  from time import time
  p = OptionParser()
  p.add_option('--term', dest='term')
  p.add_option('--all', dest='all', default=False, action="store_true")
  p.add_option('--from', dest='after')
  p.add_option('-o', dest="filename")
  (opt, args) = p.parse_args()

  if opt.all:
    terms = list(fetch_terms())
  elif opt.term:
    terms = [opt.term]
  elif opt.after:
    terms = [x for x in fetch_terms() if x >= opt.after]
  else:
    print "Need term specification."
    p.print_usage()
    sys.exit(0)

  if opt.filename:
    f = open(opt.filename, "w")
  else:
    f = sys.stdout
  
  print "Fetching terms: %s" % terms
  for term in terms:
    s = time()
    print >>sys.stderr, "\tFetching", term,
    print >>f, fetch_myc(term, fetch_subjects(term)).lower()
    print >>sys.stderr, "in %.2f seconds" % (time()-s)
  f.close()
