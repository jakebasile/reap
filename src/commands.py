from json import loads
from base64 import b64encode
from urllib2 import Request, urlopen
from keyring import set_password, get_password
from os.path import expanduser, exists
from pickle import dump, load

STATUS_TASK_FORMAT = '''Project:    {entry[project]}
Task:       {entry[task]}
ID:         {entry[project_id]} {entry[task_id]}
Notes:      {entry[notes]}
Hours:      {entry[hours]}
'''

def save_info(base_uri, username):
    with open(expanduser('~/.harvestrc'), 'w') as file:
        file.write(base_uri + '\n')
        file.write(username + '\n')

def load_info():
    with open(expanduser('~/.harvestrc'), 'r') as file:
        base_uri = file.readline().strip()
        username = file.readline().strip()
        return (base_uri, username)

def save_bookmarks(bookmarks):
    with open(expanduser('~/.harvestbkmrks'), 'w') as file:
        dump(bookmarks, file)

def load_bookmarks():
    path = expanduser('~/.harvestbkmrks')
    if exists(path):
        with open(path, 'r') as file:
            return load(file)
    else:
        return {}

def get_request(path):
    info = load_info()
    base_uri = info[0]
    username = info[1]
    passwd = get_password(base_uri, username)
    if passwd:
        auth = b64encode(username + ':' + passwd)
        uri = base_uri + path
        request = Request(uri)
        request.add_header('Content-Type', 'application/json')
        request.add_header('Accept', 'application/json')
        request.add_header('Authorization', 'Basic ' + auth)
        return request
    else:
        print 'Login first!'
        return None

def login(args):
    base_uri = 'https://' + args.subdomain + '.harvestapp.com/'
    auth = b64encode(args.username + ':' + args.password)
    uri = base_uri + 'account/who_am_i'
    request = Request(uri)
    request.add_header('Content-Type', 'application/json')
    request.add_header('Accept', 'application/json')
    request.add_header('Authorization', 'Basic ' + auth)
    try:
        response = urlopen(request)
        set_password(base_uri, args.username, args.password)
        save_info(base_uri, args.username)
        print 'Success!'
    except:
        print 'Failure, check info and try again.'

def status(args):
    request = get_request('daily')
    if request:
        response = urlopen(request)
        json = loads(''.join([line for line in response.readlines()]))
        print '\nToday\'s Projects:'
        for entry in json['day_entries']:
            if entry.has_key('timer_started_at'):
                print '**Currently Running Timer**\n',
            print str.format(STATUS_TASK_FORMAT, entry = entry)

def bookmark(args):
    bookmarks = load_bookmarks()
    bookmarks[args.name] = (args.projectid, args.taskid)
    save_bookmarks(bookmarks)

def bookmarks(args):
    bookmarks = load_bookmarks()
    print '\nCurrent Bookmarks:'
    for key in bookmarks.keys():
        bkmk = bookmarks[key]
        print str.format('{}: P:[{}] T:[{}]', key, bkmk[0], bkmk[1])
    print ''
