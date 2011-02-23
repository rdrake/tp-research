# Does awful things.  Downloads 50k HTML pages.  Don't ever do this.
from urllib2 import build_opener, HTTPError, URLError

BASE_URL = "http://ssbprod1.aac.mycampus.ca/pls/prod/www_directory.directory_uoit.p_showindividual?home_url_in=&individual_id_in="

opener = build_opener()
opener.addheaders = [("User-agent", "TP-Crawler/1.0")]

for i in range(50000):
  try:
    r = opener.open("%s%d" % (BASE_URL, i))
    data = r.read()
    f = open("%d.html" % i, "w")
    f.write(data)
  except HTTPError:
    print "Failed to open page %d." % i
  except URLError:
    print "URL error!"
