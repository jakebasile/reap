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

from reap.support import *
from reap.constants import *

import reap.api
import reap.support
import urllib2
import keyring

from json import loads, dumps
from base64 import b64encode
from urllib2 import Request, urlopen
from keyring import set_password, get_password
from os.path import expanduser, exists
from pickle import dump, load
from re import compile, IGNORECASE
from getpass import getpass

def login(args):
    password = getpass()
    try:
        print args.baseuri
        ts = reap.api.Timesheet(args.baseuri, args.username, password)
    except ValueError:
        print 'Invalid Credentials.'
        return
    except urllib2.URLError:
        print 'Unable to communicate. Check information and try again.'
        return
    keyring.set_password(args.baseuri, args.username, password)
    reap.support.save_info(args.baseuri, args.username)
    print 'You are now logged in.'

def status(args):
    ts = reap.support.get_timesheet()
    total = 0
    running_entry = None
    stopped_entries = []
    for entry in ts.entries():
        if entry.started:
            running_entry = entry
        else:
            stopped_entries += [entry]
        total += entry.hours
    if running_entry:
        print '# Currently Running Timer:'
        print str.format(
            STATUS_TASK_FORMAT,
            entry = running_entry,
            hours = int(running_entry.hours),
            minutes = int(running_entry.hours % 1 * 60),
        )
    if len(stopped_entries) > 0:
        print '# Stopped Entries:'
        for entry in stopped_entries:
            print str.format(
                STATUS_TASK_FORMAT,
                entry = entry,
                hours = int(entry.hours),
                minutes = int(entry.hours % 1 * 60),
            )

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

def note(args):
    task_info = get_task_info(args.task)
    entry = get_entry(task_info[0], task_info[1])
    if args.append:
        entry['notes'] = entry['notes'] + args.note
    else:
        entry['notes'] = args.note
    request = get_request('daily/update/' + str(entry['id']))
    request.add_data(dumps(entry))
    response = urlopen(request)
    if response.code == 200:
        print 'Success!'

def start(args):
    task_info = get_task_info(args.task)
    entry = get_entry(task_info[0], task_info[1])
    if not entry:
        # entry not found, need to create it.
        req = {
            'notes': '',
            'hours': '',
            'project_id': task_info[0],
            'task_id': task_info[1],
        }
        request = get_request('daily/add')
        request.add_data(dumps(req))
        response = urlopen(request)
        if response.code == 200:
            print 'Timer Started!'
    else:
        request = get_request('daily/timer/' + str(entry['id']))
        response = urlopen(request)
        if response.code == 200:
            print 'Timer Started!'

def stop(args):
    active = get_active_timer()
    if active:
        request = get_request('daily/timer/' + str(active['id']))
        response = urlopen(request)
        if response.code == 200:
            print 'Timer stopped!'
    else:
        print 'No active timer!'

def delete(args):
    task_info = get_task_info(args.task)
    entry = get_entry(task_info[0], task_info[1])
    if not entry:
        print 'No task found.'
    else:
        request = get_request('daily/delete/' + str(entry['id']))
        response = urlopen(request)
        if response:
            print 'Task deleted'
