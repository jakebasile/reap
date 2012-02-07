from json import loads
from base64 import b64encode
from urllib2 import Request, urlopen

def login(args):
    base_uri = 'https://' + args.subdomain + '.harvestapp.com/'
    auth = b64encode(args.username + ':' + args.password)
    uri = base_uri + 'account/who_am_i'
    request = Request(uri)
    request.add_header('Content-Type', 'application/json')
    request.add_header('Accept', 'application/json')
    request.add_header('Authorization', 'Basic ' + auth)
    response = urlopen(request)
    if response.code == 200:
        print 'Success!'
    else:
        print 'Failure, check info and try again.'
