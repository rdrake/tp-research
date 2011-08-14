import fileinput as fi
import re

"""BIOL 1010U Biology I: Molecular and Cellular Systems. This course examines the evolutionary basis of life at the cellular level. Topics will include the basic structure and function of cells, cell energetics and respiration, photosynthesis, the structure and function of DNA, the control of gene expression, cell division and the evolution of multicellularity. 3 cr, 3 lec, 3 lab (biweekly), 1.5 tut (biweekly). Prerequisites: Grade 12 Biology (SBI4U) (recommended). Credit restriction: BIOL 1840U. Note: Students without the biology prerequisite will be responsible for making up background material."""
#regexp = re.compile(r'^([A-Z]{4}\s{1}[0-9]{4}[G|U])([^\.])(.+)')
regexp = re.compile(r'^([A-Z]{4}\s{1}[0-9]{4}[G|U])([^\.]+)[\.\s+](.+)')
courses = []

for line in fi.input():
	m = regexp.match(line)
	
	if m:
		print "|".join(map(lambda s: s.strip(), m.group(1, 2, 3)))
		#courses.append(m.group(1, 2, 3))
