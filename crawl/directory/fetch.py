BASE_URL = "http://ssbprod1.aac.mycampus.ca/pls/prod/"
DEPTS_URL = BASE_URL + "www_directory.directory_uoit.p_main"
PRSNS_URL = BASE_URL + "www_directory.directory_uoit.p_ShowDepartment?department_name_in="

from lxml import html
from time import sleep
from urllib2 import urlopen

depts_html = urlopen(DEPTS_URL)
depts_doc = html.parse(depts_html)
depts_ids = [option.values()[0] for option in depts_doc.findall(".//option")]

dir_hrefs = []

# Iterate through all departments, grabbing all links to employee information pages.
for dept_id in depts_ids:
	depts_staff_html = urlopen(PRSNS_URL + dept_id)
	depts_staff_doc = html.parse(depts_staff_html)
	dir_hrefs.extend([person.attrib["href"] for person in depts_staff_doc.findall(".//td/a[@href]")])

current = 0
total = len(dir_hrefs)

for href in dir_hrefs:
	current += 1
	print "Grabbing article %s (%d of %d)" % (href, current, total)

	f = open("%s.html" % href, "w")
	doc = urlopen(BASE_URL + href)

	f.write(doc.read())

	sleep(0.1)
