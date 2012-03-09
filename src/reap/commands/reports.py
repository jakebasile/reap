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

import keyring
import getpass
import urllib2
import reap.api.admin
import datetime
from reap.commands.support import *

REPORT_HEADER = '''{} Report:
    From: {}
    To: {}
    Results:'''

HOURS_REPORT_FORMAT = '''    -   Name:           {person.first_name} {person.last_name}
        ID:             {person.id}
        Total Hours:    {total}
        Billable:       {billable}
        Non-billable:   {unbillable}
        Ratio B/NB:     {ratio:.2%}
        Ratio B/Total:  {percent:.2%}
'''

PERSON_PROJECTS_REPORT_HEADING_FORMAT = \
'''    -   Name:           {person.first_name} {person.last_name}
        Projects:'''

PERSON_PROJECTS_REPORT_BODY_FORMAT = '''        -   Name:       {name}
            Hours:      {hours}'''

TASKS_HEADER_FORMAT = '''    -   Name:   {person.first_name} {person.last_name}
        Tasks:'''

TASKS_BODY_FORMAT = '''        -   Task:   {name}
            Hours:  {hours}'''

def get_harvest():
    info = load_info()
    if info:
        base_uri = info[0]
        username = info[1]
        passwd = keyring.get_password(base_uri, username)
        return reap.api.admin.Harvest(base_uri, username, passwd)

def get_people(hv, ids):
    people = []
    all_people = hv.people()
    for pid in set(ids):
        id = int(pid)
        for p in all_people:
            if p.id == id:
                people += [p]
                break
    return people

def parse_time_inputs(startstr, endstr):
    if startstr:
        start = datetime.datetime.strptime(startstr, '%Y%m%d')
    else:
        start = datetime.datetime.today()
    if endstr:
        end = datetime.datetime.strptime(endstr, '%Y%m%d')
    else:
        end = datetime.datetime.today()
    return (start, end)

def hours(args):
    hv = get_harvest()
    if hv:
        people = get_people(hv, args.personids)
        if len(people) > 0:
            times = parse_time_inputs(args.start, args.end)
            start = times[0]
            end = times[1]
            entries_collection = [
                (person, person.entries(start = start, end = end))
                for person in people
            ]
            if len(entries_collection) > 0:
                print str.format(
                    REPORT_HEADER,
                    'Hours',
                    start.strftime('%Y-%m-%d'),
                    end.strftime('%Y-%m-%d'),
                )
                overall_hours = 0.0
                overall_billable = 0.0
                projects = hv.projects()
                for person, entries in entries_collection:
                    map = {p: [] for p in projects}
                    for entry in entries:
                        for proj in map.keys():
                            if proj.id == entry.project_id:
                                map[proj] += [entry]
                                break;
                    total = 0.0
                    billable = 0.0
                    unbillable = 0.0
                    for proj in map.keys():
                        proj_total = 0.0
                        for entry in map[proj]:
                            proj_total += entry.hours
                        overall_hours += proj_total
                        if proj.billable:
                            billable += proj_total
                            overall_billable += proj_total
                        else:
                            unbillable += proj_total
                        total += proj_total
                    # Divide by zero is undefined, but fudge it a little bit
                    # for easier output.
                    ratio = billable / unbillable if unbillable > 0.0 else 0.0
                    percent = billable / total if total > 0.0 else 0.0
                    print str.format(
                        HOURS_REPORT_FORMAT,
                        total = total,
                        billable = billable,
                        unbillable = unbillable,
                        ratio = ratio,
                        person = person,
                        percent = percent,
                    )
                print str.format(
                    'Overall Billable: {:.2%}',
                    overall_billable / overall_hours if overall_hours != 0.0 else 0
                )
            else:
                print 'No entries for that time period.'
        else:
            print 'No such person ID(s).'

def projects(args):
    hv = get_harvest()
    if hv:
        people = get_people(hv, args.personids)
        if len(people) > 0:
            times = parse_time_inputs(args.start, args.end)
            start = times[0]
            end = times[1]
            projects = hv.projects()
            projects_by_id = {project.id: project for project in projects}
            print str.format(
                REPORT_HEADER,
                'Projects',
                start.strftime('%Y-%m-%d'),
                end.strftime('%Y-%m-%d'),
            )
            for person in people:
                print str.format(PERSON_PROJECTS_REPORT_HEADING_FORMAT, person = person)
                person_projects = {}
                for entry in person.entries(start = start, end = end):
                    project = projects_by_id[entry.project_id]
                    if person_projects.has_key(project):
                        person_projects[project] += entry.hours
                    else:
                        person_projects[project] = entry.hours
                for project in person_projects.keys():
                    print str.format(
                        PERSON_PROJECTS_REPORT_BODY_FORMAT,
                        name = project.name,
                        hours = person_projects[project]
                    )
        else:
            print 'No such person ID(s).'

def tasks(args):
    hv = get_harvest()
    if hv:
        people = get_people(hv, args.personids)
        if len(people) > 0:
            times = parse_time_inputs(args.start, args.end)
            start = times[0]
            end = times[1]
            tasks = hv.tasks()
            tasks_by_id = {task.id: task for task in tasks}
            print str.format(
                REPORT_HEADER,
                'Tasks',
                start.strftime('%Y-%m-%d'),
                end.strftime('%Y-%m-%d'),
            )
            for person in people:
                print str.format(TASKS_HEADER_FORMAT, person = person)
                person_tasks = {}
                for entry in person.entries(start = start, end = end):
                    task = tasks_by_id[entry.task_id]
                    if person_tasks.has_key(task):
                        person_tasks[task] += entry.hours
                    else:
                        person_tasks[task] = entry.hours
                for task in person_tasks.keys():
                    print str.format(
                        TASKS_BODY_FORMAT,
                        name = task.name,
                        hours = person_tasks[task]
                    )
        else:
            print 'No such person ID(s).'
