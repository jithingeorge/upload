#! /usr/bin/python
import requests, logging, json
from random import randint
from akamai.edgegrid import EdgeGridAuth
from config import EdgeGridConfig
from urlparse import urljoin
import urllib

session = requests.Session()
debug = False

# Config contains the values set in .edgerc (tokens, URL)
config = EdgeGridConfig({},"default")

# Debug code was present in the sample example, so I just used it here. Required?
if hasattr(config, 'verbose'):
	debug = config.verbose

if debug:
  import httplib as http_client
  http_client.HTTPConnection.debuglevel = 1
  logging.basicConfig()
  logging.getLogger().setLevel(logging.DEBUG)
  requests_log = logging.getLogger("requests.packages.urllib3")
  requests_log.setLevel(logging.DEBUG)
  requests_log.propagate = True


# Creating the digital signature for the request and updating headers
session.auth = EdgeGridAuth(
            client_token=config.client_token,
            client_secret=config.client_secret,
            access_token=config.access_token
)

if hasattr(config, 'headers'):
	session.headers.update(config.headers)

# debug info
#print config.host

# Forming end point
baseurl = '%s://%s/' % ('https', config.host)

# Sending request to data API in audience-analytics group. Details in mail
result = session.get(urljoin(baseurl, 
     '/media-analytics/v1/audience-analytics/report-packs/28354/data?startDate=12/01/2014&endDate=12/03/2014&dimensions=12&metrics=117&aggregation=60&limit=10000'))

# Just printing out the json dump
print json.dumps(result.json(), indent=2)

