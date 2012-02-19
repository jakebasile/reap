# Copyright 2012 Jake Basile
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from reap.constants import *

import reap.api

from json import loads, dumps
from base64 import b64encode
from urllib2 import Request, urlopen
from keyring import set_password, get_password
from os.path import expanduser, exists
from pickle import dump, load
from re import compile, IGNORECASE

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

def get_timesheet():
    info = reap.support.load_info()
    base_uri = info[0]
    username = info[1]
    passwd = get_password(base_uri, username)
    return reap.api.Timesheet(base_uri, username, passwd)


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
        request.add_header('User-Agent', 'reap')
        return request
    else:
        print 'Login first!'
        return None

def get_task_info(query):
    # check for id in bookmarks first.
    bkmks = load_bookmarks()
    if bkmks.has_key(query):
        return bkmks[query]
    # If it's not there, get the full list and search it.
    request = get_request('daily')
    if request:
        response = urlopen(request)
        json = loads(''.join([line for line in response.readlines()]))
        projects = json['projects']
        q = compile(query, IGNORECASE)
        results = []
        for project in projects:
            for task in project['tasks']:
                matches = q.search(task['name'])
                if matches:
                    results += [(project, task)]
        # if there is only one search result, return it now.
        if len(results) is 1:
            return (results[0][0]['id'], results[0][1]['id'])
        # otherwise, ask the user.
        print '\nMore than one task found, please select task from list.\n'
        i = 1
        for project, task in results:
            print str.format(SELECT_TASK_FORMAT, project = project, task = task, index = i)
            i += 1
        selection = None
        while not selection:
            print 'Choose Wisely: ',
            input = raw_input()
            try:
                candidate = int(input) - 1
                if candidate >= 0 and candidate < len(results):
                    selection = candidate
                else:
                    print 'You have chosen... poorly.'
            except:
                print 'You have chosen... poorly.'
        return (results[selection][0]['id'], results[selection][1]['id'])

def get_entry(projectid, taskid):
    # im not really sure why this needs to happen.
    projectid = str(projectid)
    taskid = str(taskid)
    request = get_request('daily')
    if request:
        response = urlopen(request)
        json = loads(''.join([line for line in response.readlines()]))
        entries = json['day_entries']
        for entry in entries:
            if entry['project_id'] == projectid and entry['task_id'] == taskid:
                return entry
        # TODO: what about multiple entries with the same task info?

def get_active_timer():
    request = get_request('daily')
    if request:
        response = urlopen(request)
        json = loads(''.join([line for line in response.readlines()]))
        entries = json['day_entries']
        for entry in entries:
            if entry.has_key('timer_started_at'):
                return entry
