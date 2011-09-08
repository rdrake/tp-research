#!/bin/bash
now=`date +%Y%m`
python fetch.py --from $now \
| java -jar parse.jar \
| python store.py --url=sqlite:///mycampu_$now.sq3
