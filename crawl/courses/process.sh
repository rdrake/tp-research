#!/bin/bash
filename=$(basename $1)			# Get the base filename
filenoext=${filename%.*}		# Remove the extension
newfilename=$filenoext.txt	# Append the new extension
PYTHON=/usr/bin/python2			# Path to Python executable to run.

# Converts the PDF to raw text, strips out line numbers and other garbage,
# and finally runs the resulting text through multiple sinks to achieve the
# purified course information.
pdftotext -raw $1 - | grep -Ev '(^[0-9]{3}$)|SECTION|(UNDER|)GRADUATE COURSE DESCRIPTIONS' | $PYTHON massage.py | $PYTHON extract_course_info.py
