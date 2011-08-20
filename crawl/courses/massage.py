import fileinput as fi
import re

courses = []
acc = []
regexp = re.compile(r'^[A-Z]{4}\s{1}[0-9]{4}(U|G)\s{1}[A-Z]{1}.')

def start_of_line(s):
	return bool(regexp.search(s))

for line in fi.input():
	# Skip the current line if it's too large.
	if len(line) >= 60:
		continue
	
	if start_of_line(line):
		# The 2011-2012 calendar has all text set to justify, need to fix that.
		course_info = re.sub(r'\s+', ' ', " ".join(acc))
		courses.append(course_info)
		print course_info
		del acc[:]
	
	acc.append(line.strip())
