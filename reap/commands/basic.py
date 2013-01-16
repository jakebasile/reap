# Copyright 2012-2013 Jake Basile
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

import keyring
import getpass
import urllib2
import re
import reap.api.timesheet
from reap.commands.support import *

STATUS_TASK_FORMAT = '''{indicator}   Project:    {entry.project_name}
    Task:       {entry.task_name}
    ID:         {entry.id}
    Notes:      {entry.notes}
    Time:       {hours}:{minutes:02d}
'''

def get_timesheet():
    info = load_info()
    if info:
        base_uri = info[0]
        username = info[1]
        passwd = keyring.get_password(base_uri, username)
        return reap.api.timesheet.Timesheet(base_uri, username, passwd)

def get_entry(ts, entryid):
    entries = ts.entries()
    try:
        id = int(entryid)
    except ValueError:
        # the entry is not an ID.
        regex = re.compile(entryid, flags = re.IGNORECASE)
        matches = []
        for entry in entries:
            if regex.search(entry.task_name):
                matches += [entry]
        if len(matches) is 1:
            return matches[0]
        elif len(matches) >= 2:
            print 'More than one match found. Narrow your search.'
            return None
    else:
        # the entry is an ID.
        for entry in entries:
            if entry.id == id:
                return entry

def login(args):
    password = getpass.getpass()
    try:
        ts = reap.api.timesheet.Timesheet(args.baseuri, args.username, password)
    except ValueError:
        print 'Invalid Credentials.'
        return
    except urllib2.URLError:
        print 'Unable to communicate. Check information and try again.'
        return
    keyring.set_password(args.baseuri, args.username, password)
    save_info(args.baseuri, args.username)
    print 'You are now logged in.'

def status(args):
    ts = get_timesheet()
    if ts:
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
            print 'Currently Running Timer:'
            print str.format(
                STATUS_TASK_FORMAT,
                entry = running_entry,
                hours = int(running_entry.hours),
                minutes = int(running_entry.hours % 1 * 60),
                indicator = ' '
            )
        if len(stopped_entries) > 0:
            print 'Stopped Entries:'
            for entry in stopped_entries:
                print str.format(
                    STATUS_TASK_FORMAT,
                    entry = entry,
                    hours = int(entry.hours),
                    minutes = int(entry.hours % 1 * 60),
                    indicator = '-'
                )
        if total:
            total_hours = int(total)
            total_minutes = int(total % 1 * 60)
            print str.format('Total Daily Hours: {}:{:02d}\n', total_hours, total_minutes)

def start(args):
    ts = get_timesheet()
    if ts:
        found = get_entry(ts, args.entryid)
        if found:
            if found.started:
                print 'Entry timer already started.'
            else:
                found.start()
                print 'Entry timer started.'
        else:
            print 'No entry with that ID or matching that regex.'

def stop(args):
    ts = get_timesheet()
    if ts:
        found = None
        for entry in ts.entries():
            if entry.started:
                found = entry
                break
        if found:
            found.stop()
            print 'Entry timer stopped.'
        else:
            print 'No timers to stop.'

def list(args):
    ts = get_timesheet()
    if ts:
        print 'Projects and Tasks:'
        for proj in ts.projects():
            print '    - ' + proj.name + ':'
            for task in proj.tasks():
                print str.format('        - {} ({} {})', task.name, proj.id, task.id)
            print ''

def create(args):
    ts = get_timesheet()
    if ts:
        dec_time = 0.0
        if args.time:
            split = args.time.split(':')
            hours = float(split[0])
            minutes = float(split[1])
            dec_time = hours + minutes / 60
        notes = args.notes or ''
        for proj in ts.projects():
            if proj.id == int(args.projectid):
                for task in proj.tasks():
                    if task.id == int(args.taskid):
                        entry = ts.create_entry(proj.id, task.id, hours = dec_time, notes = notes)
                        print 'Added Entry:'
                        print str.format(
                            STATUS_TASK_FORMAT,
                            entry = entry,
                            hours = int(entry.hours),
                            minutes = int(entry.hours % 1 * 60),
                            indicator = ' '
                        )
                        return
        print 'No project/task found with those IDs.'

def delete(args):
    ts = get_timesheet()
    if ts:
        found = get_entry(ts, args.entryid)
        if found:
            found.delete()
            print 'Entry deleted.'
        else:
            print 'No entry with that ID.'

def update(args):
    ts = get_timesheet()
    if ts:
        found = get_entry(ts, args.entryid)
        if found:
            time = found.hours
            proj_id = found.project_id
            task_id = found.task_id
            notes = found.notes
            # check for notes
            if args.notes:
                if args.append:
                    notes = found.notes + args.notes
                else:
                    notes = args.notes
            # check for time
            if args.time:
                split = args.time.split(':')
                hours = float(split[0])
                minutes = float(split[1])
                time = hours + minutes / 60
                if args.append:
                    time = found.hours + time
            # check for task.
            if args.task:
                found_task = None
                for proj in ts.projects():
                    if proj.id == int(args.task[0]):
                        for task in proj.tasks():
                            if task.id == int(args.task[1]):
                                found_task = task
                                break
                if found_task:
                    proj_id = args.task[0]
                    task_id = args.task[1]
                else:
                    print 'No such project and task ID. Abort.'
                    return
            found.update(notes, time, proj_id, task_id)
            print 'Updated Entry:'
            print str.format(
                STATUS_TASK_FORMAT,
                entry = found,
                hours = int(found.hours),
                minutes = int(found.hours % 1 * 60),
                indicator = ' '
            )
        else:
            print 'No entry with that ID.'

