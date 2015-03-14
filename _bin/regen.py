#!/usr/bin/env python2
from __future__ import print_function

import urllib2
import json
import sys
import os

def log(msg):
    print(msg)

def get(url):
    return urllib2.urlopen(url).read()

log('Getting api rate limit')
rate = json.loads(get('https://api.github.com/rate_limit'))

remaining = [
    rate['resources']['core']['remaining'],
    rate['resources']['search']['remaining'],
    rate['rate']['remaining'],
]
if any([r < 5 for r in remaining]):
    log('API limit too low')
    sys.exit(1)
log('API limit acceptable')

scriptdir = os.path.dirname(os.path.abspath(__file__))
targetpath = os.path.join(os.path.dirname(scriptdir), 'data', 'repos.json')

log('Getting repos list')
repos = get('https://api.github.com/orgs/docker-in-practice/repos')
log('Got repos list, writing')
with open(targetpath, 'w') as f:
    f.write(repos)
