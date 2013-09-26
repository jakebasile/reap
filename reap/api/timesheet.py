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

from reap.api.base import ReapBase, parse_time

class Timesheet(ReapBase):
    def __init__(self, base_uri, username, password):
        self.base_uri = base_uri
        self.username = username
        self.password = password
        login_response = self.get_request('account/who_am_i')
        if not login_response:
            raise ValueError('Unable to login with given info.')
        self.id = login_response['user']['id']

    def projects(self):
        projects_response = self.get_request('daily')
        projects = [Project(pjson) for pjson in projects_response['projects']]
        return projects

    def entries(self, day_of_year = None, year = None):
        if(day_of_year and year):
            entries_response = self.get_request('daily/' + str(day_of_year) + '/' + str(year))
        else:
            entries_response = self.get_request('daily')
        
        entries = [Entry(self, ejson) for ejson in entries_response.get('day_entries')]
        return entries

    def create_entry(self, project_id, task_id, hours = 0, notes = '', spent_at = ''):
        entry = {
            'project_id': project_id,
            'task_id': task_id,
            'hours': hours,
            'notes': notes,
            'spent_at': spent_at
        }
        response = self.post_request('daily/add', entry)
        if response:
            return Entry(self, response)

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

class Entry:
    def __init__(self, ts, json):
        self.ts = ts
        self.__parse_json(json)

    def __parse_json(self, json):
        self.id = json['id']
        self.spent_at = json['spent_at']
        self.user_id = json['user_id']
        self.client_name = json['client']
        # workaround because sometimes this comes back as a string, not an int.
        self.project_id = int(json['project_id'])
        self.project_name = json['project']
        # workaround because sometimes this comes back as a string, not an int.
        self.task_id = int(json['task_id'])
        self.task_name = json['task']
        self.hours = json['hours']
        # sometimes this is None, set None to empty string.
        self.notes = json['notes'] or ''
        self.started = json.has_key('timer_started_at')
        if self.started:
            self.timer_started = parse_time(json['timer_started_at'])
            self.timer_created = parse_time(json['created_at'])
            self.timer_updated = parse_time(json['updated_at'])
        else:
            self.timer_started = None
            self.timer_created = None
            self.timer_updated = None

    def delete(self):
        response = self.ts.get_request('daily/delete/' + str(self.id))

    def update(self, notes = None, hours = None, project_id = None, task_id = None):
        changes = {}
        if notes:
            changes['notes'] = notes
        if hours:
            changes['hours'] = hours
        if project_id:
            changes['project_id'] = project_id
        if task_id:
            changes['task_id'] = task_id
        if(len(changes) > 0):
            response = self.ts.post_request('daily/update/' + str(self.id), changes)
            if response:
                new_info = self.ts.get_request('daily/show/' + str(self.id))
                self.__parse_json(new_info)

    def start(self):
        if not self.started:
            response = self.ts.get_request('daily/timer/' + str(self.id))
            if response:
                new_info = self.ts.get_request('daily/show/' + str(self.id))
                self.__parse_json(new_info)

    def stop(self):
        if self.started:
            response = self.ts.get_request('daily/timer/' + str(self.id))
            if response:
                new_info = self.ts.get_request('daily/show/' + str(self.id))
                self.__parse_json(new_info)
