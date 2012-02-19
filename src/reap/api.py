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
import reap.constants

class Timesheet:
    def __init__(self, base_uri, username, password):
        self.base_uri = 'https://' + base_uri + '.harvestapp.com/'
        self.username = username
        self.password = password
        login_response = self.__get_request('account/who_am_i')
        if not login_response:
            raise ValueError('Unable to login with given info.')

    def __get_request(self, path):
        auth = base64.b64encode(self.username + ':' + self.password)
        uri = self.base_uri + path
        request = urllib2.Request(uri)
        request.add_header('Content-Type', 'application/json')
        request.add_header('Accept', 'application/json')
        request.add_header('Authorization', 'Basic ' + auth)
        request.add_header('User-Agent', 'reap')
        result = urllib2.urlopen(request)
        result_json = json.load(result)
        return result_json

    def projects(self):
        projects_response = self.__get_request('daily')
        projects = [Project(pjson) for pjson in projects_response['projects']]
        return projects

    def entries(self):
        entries_response = self.__get_request('daily')
        entries = Entries(entries_response['day_entries'])
        return entries

class Project:
    def __init__(self, json):
        self.name = json['name']
        self.id = json['id']
        self.client = json['client']
        self.task_json = json['tasks']

    def tasks(self):
        tasks = [Task(tjson) for tjson in self.task_json]
        return tasks

class Task:
    def __init__(self, json):
        self.name = json['name']
        self.id = json['id']
        self.billable = json['billable']

class Entries:
    def __init__(self, json):
        self.entry_list = [Entry(ejson) for ejson in json]

    def __iter__(self):
        return iter(self.entry_list)

class Entry:
    def __init__(self, json):
        self.id = json['id']
        self.spent_at = json['spent_at']
        self.user_id = json['user_id']
        self.client_name = json['client']
        self.project_id = json['project_id']
        self.project_name = json['project']
        self.task_id = json['task_id']
        self.task_name = json['task']
        self.hours = json['hours']
        self.notes = json['notes']
        self.started = json.has_key('timer_started_at')
        if self.started:
            self.timer_started = json['started_at']
            self.timer_started = json['created_at']
            self.timer_started = json['updated_at']
