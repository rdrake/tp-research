#!/bin/bash
#now=`date +%Y%m`
now=201109
python fetch.py --from $now \
| java -jar parse.jar \
| python store.py --url=sqlite:///mycampus_$now.sq3
