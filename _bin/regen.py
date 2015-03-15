#!/usr/bin/env python2
from __future__ import print_function

import urllib2
import json
import sys
import os
import re

SCRIPTDIR = os.path.dirname(os.path.abspath(__file__))
DATADIR = os.path.join(os.path.dirname(SCRIPTDIR), 'data')

def log(msg, *args):
    print(msg % args)

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

repolistre = '''<a href="/u/dockerinpractice/([^/"']+)/"><div class="repo-list-item box">'''
repoprojre = '''https://github\.com/docker-in-practice/([^/"']+)\.git'''
def get_dockerhub_data():
  log('Getting DH data!')
  reposhtml = get('https://registry.hub.docker.com/repos/dockerinpractice/')
  log('Scraping repo names')
  reponames = re.findall(repolistre, reposhtml)
  assert len(reponames) > 0

  repos = []
  log('Got repos list, getting details for each repo')
  baserepourl = 'https://registry.hub.docker.com/u/dockerinpractice/'
  for i, reponame in enumerate(reponames):
      log('%s/%s - %s', i+1, len(reponames), reponame)
      url = baserepourl + reponame + '/'
      repohtml = get(url)
      assert 'AUTOMATED BUILD REPOSITORY' in repohtml, reponame + " not automated"
      repoprojs = re.findall(repoprojre, repohtml)
      assert len(repoprojs) == 1, "Got %s for %s" % (repoprojs, reponame)
      repos.append({ "name": reponame, "github_name": repoprojs[0], "url": url })

  with open(os.path.join(DATADIR, 'dhrepos.json'), 'w') as f:
      json.dump(repos, f)

get_github_data()
get_dockerhub_data()
