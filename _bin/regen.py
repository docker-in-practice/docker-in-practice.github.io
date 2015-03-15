#!/usr/bin/env python2
from __future__ import print_function

import urllib2
import json
import sys
import os
import re

SCRIPTDIR = os.path.dirname(os.path.abspath(__file__))
DATADIR = os.path.join(os.path.dirname(SCRIPTDIR), 'data')

def log(msg):
    print(msg)

def get(url):
    return urllib2.urlopen(url).read()

def get_github_data():
  log('Getting GH data!')
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


  log('Getting repos list')
  repos = get('https://api.github.com/orgs/docker-in-practice/repos')
  log('Got repos list, writing')
  with open(os.path.join(DATADIR, 'ghrepos.json'), 'w') as f:
      f.write(repos)

def get_dockerhub_data():
  log('Getting DH data!')
  reposhtml = get('https://registry.hub.docker.com/repos/dockerinpractice/')
  log('Extracting repos list')
  reposre = '<a href="/u/dockerinpractice/([^/]+)/"><div class="repo-list-item box">'
  repos = re.findall(reposre, reposhtml)
  assert len(repos) != 0
  log('Got repos list, writing')
  with open(os.path.join(DATADIR, 'dhrepos.json'), 'w') as f:
      json.dump(repos, f)

get_github_data()
get_dockerhub_data()
