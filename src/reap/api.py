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

import urllib2
import json
import base64
import datetime

def parse_time(timestr):
    return datetime.datetime.strptime(timestr, '%Y-%m-%dT%H:%M:%SZ')

class Timesheet:
    def __init__(self, base_uri, username, password):
        self.base_uri = 'https://' + base_uri + '.harvestapp.com/'
        self.username = username
        self.password = password
        login_response = self.get_request('account/who_am_i')
        if not login_response:
            raise ValueError('Unable to login with given info.')

    def __init_request(self, path):
        auth = base64.b64encode(self.username + ':' + self.password)
        uri = self.base_uri + path
        request = urllib2.Request(uri)
        request.add_header('Content-Type', 'application/json')
        request.add_header('Accept', 'application/json')
        request.add_header('Authorization', 'Basic ' + auth)
        request.add_header('User-Agent', 'reap')
        return request

    def get_request(self, path):
        request = self.__init_request(path)
        result = urllib2.urlopen(request)
        result_json = json.load(result)
        return result_json

    def post_request(self, path, data):
        request = self.__init_request(path)
        request.add_data(json.dumps(data))
        result = urllib2.urlopen(request)
        result_json = json.load(result)
        return result_json

    def projects(self):
        projects_response = self.get_request('daily')
        projects = [Project(pjson) for pjson in projects_response['projects']]
        return projects

    def entries(self):
        entries_response = self.get_request('daily')
        entries = Entries(self, entries_response['day_entries'])
        return entries

class Project:
    def __init__(self, json):
        self.name = json['name']
        self.id = json['id']
        self.client = json['client']
        self.task_json = json['tasks']

    def tasks(self):
        tasks = [Task(self, tjson) for tjson in self.task_json]
        return tasks

class Task:
    def __init__(self, project, json):
        self.name = json['name']
        self.id = json['id']
        self.billable = json['billable']
        self.project = project

class Entries:
    def __init__(self, ts, json):
        self.ts = ts
        self.entry_list = [Entry(ejson) for ejson in json]

    def __iter__(self):
        return iter(self.entry_list)

    def create(self, task, hours = 0, notes = ''):
        entry = {
            'project_id': task.project.id,
            'task_id': task.id,
            'hours': hours,
            'notes': notes,
        }
        response = self.ts.post_request('daily/add', entry)
        if response:
            return Entry(response)

class Entry:
    def __init__(self, json):
        self.id = json['id']
        self.spent_at = json['spent_at']
        self.user_id = json['user_id']
        self.client_name = json['client']
        # workaround because sometimes this comes back as a string, not an int.
        self.project_id = int(json['project_id'])
        self.project_name = json['project']
        self.task_id = json['task_id']
        self.task_name = json['task']
        self.hours = json['hours']
        self.notes = json['notes']
        self.started = json.has_key('timer_started_at')
        if self.started:
            self.timer_started = parse_time(json['timer_started_at'])
            self.timer_created = parse_time(json['created_at'])
            self.timer_updated = parse_time(json['updated_at'])
        else:
            self.timer_started = None
            self.timer_created = None
            self.timer_updated = None
