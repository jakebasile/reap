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

'''An API for administrative functions on a Harvest time tracking system.'''

import datetime
from reap.api.base import ReapBase, parse_time, parse_short_time

class Harvest(ReapBase):
    '''Base class for accessing Harvest admin functions.'''
    def __init__(self, base_uri, username, password):
        '''Creates a new instance and logs the user in.

        This will send the user's username and password to Harvest and attempt
        	logging in. If the username and password given are invalid or are
        	not an administrative account, a ValueError will be thrown.'''
        self.base_uri = base_uri
        self.username = username
        self.password = password
        login_response = self.get_request('account/who_am_i')
        if not login_response:
            raise ValueError('Unable to login with given info.')
        if not login_response['user']['admin']:
            raise ValueError('User is not an admin')
        self.id = login_response['user']['id']

    def people(self):
        '''Generates a list of all People.'''
        people_response = self.get_request('people/')
        return [Person(self, pjson['user']) for pjson in people_response]

    def projects(self):
        '''Generates a list of all Projects.'''
        projects_response = self.get_request('projects/')
        return [Project(self, pjson['project']) for pjson in projects_response]

    def tasks(self):
        '''Generates a list of all Tasks.'''
        tasks_response = self.get_request('tasks/')
        return [Task(self, tjson['task']) for tjson in tasks_response]

    def clients(self):
        '''Generates a list of all Clients.'''
        clients_response = self.get_request('clients/')
        return [Client(self, cjson['client']) for cjson in clients_response]

    def get_client(self, client_id):
        '''Gets a single client by id.'''
        client_response = self.get_request('clients/%s' % client_id)
        return Client(self, client_response['client'])

    def get_project(self, project_id):
        '''Gets a single project by id.'''
        project_response = self.get_request('projects/%s' % project_id)
        return Project(self, project_response['project'])

    def create_person(self, first_name, last_name, email, department = None,
    	default_rate = None, admin = False, contractor = False):
        '''Creates a Person with the given information.'''
        person = {'user':{
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'department': department,
            'default_hourly_rate': default_rate,
            'is_admin': admin,
            'is_contractor': contractor,
        }}
        response = self.post_request('people/', person, follow = True)
        if response:
            return Person(self, response['user'])

    def create_project(self, name, client_id, budget = None, budget_by =
    	'none', notes = None, billable = True):
        '''Creates a Project with the given information.'''
        project = {'project':{
            'name': name,
            'client_id': client_id,
            'budget_by': budget_by,
            'budget': budget,
            'notes': notes,
            'billable': billable,
        }}
        response = self.post_request('projects/', project, follow = True)
        if response:
            return Project(self, response['project'])

    def create_client(self, name):
        '''Creates a Client with the given information.'''
        client = {'client':{
            'name': name,
        }}
        response = self.post_request('clients/', client, follow = True)
        if response:
            return Client(self, response['client'])

class Person:
    '''Represents a Person in the Harvest system.'''
    def __init__(self, hv, json):
        self.hv = hv
        self.id = json['id']
        self.email = json['email']
        self.first_name = json['first_name']
        self.last_name = json['last_name']
        self.all_future = json['has_access_to_all_future_projects']
        self.default_rate = json['default_hourly_rate']
        self.active = json['is_active']
        self.admin = json['is_admin']
        self.contractor = json['is_contractor']
        self.telephone = json['telephone']
        self.department = json['department']
        self.timezone = json['timezone']

    def delete(self):
        '''Deletes the person immediately.'''
        response = self.hv.delete_request('people/' + str(self.id))
        return response

    def entries(self, start = datetime.datetime.today(), end =
    	datetime.datetime.today()):
        '''Retrieves entries from all projects/tasks logged by this person.

        Can be filtered based on time by specifying start/end datetimes.'''
        fr = start.strftime('%Y%m%d')
        to = end.strftime('%Y%m%d')
        url = str.format(
            'people/{}/entries?from={}&to={}',
            str(self.id),
            fr,
            to,
        )
        response = self.hv.get_request(url)
        return [Entry(self.hv, ej['day_entry']) for ej in response]

class Entry:
    '''A timesheet entry.'''
    def __init__(self, hv, json):
        self.id = json['id']
        self.hours = float(json['hours'])
        self.project_id = json['project_id']
        self.notes = json['notes']
        self.task_id = json['task_id']
        self.user_id = json['user_id']
        self.billed = json['is_billed']
        self.closed = json['is_closed']
        self.updated = parse_time(json['updated_at'])
        self.created = parse_time(json['created_at'])
        self.spent = parse_short_time(json['spent_at'])

class Project:
    '''A project in the Harvest system.'''

    BUDGET_BY_TYPE = ['project', 'project_cost', 'task', 'person', 'none']

    def __init__(self, hv, json):
        self.hv = hv
        self.id = json['id']
        self.name = json['name']
        self.active = json['active']
        self.billable = json['billable']
        self.bill_by = json['bill_by']
        self.hourly_rate = json['hourly_rate']
        self.client_id = json['client_id']
        self.code = json['code']
        self.notes = json['notes']
        self.budget_by = json['budget_by']
        self.budget = float(json['budget']) if json['budget'] else None
        self.cost_budget = float(json['cost_budget']) if json['cost_budget'] else None
        self.latest_record = parse_short_time(json['hint_latest_record_at'])
        self.earliest_record = parse_short_time(json['hint_earliest_record_at'])
        self.created = parse_time(json['created_at'])
        self.updated = parse_time(json['updated_at'])

    def delete(self):
        '''Immediately deletes the project.'''
        response = self.hv.delete_request('projects/' + str(self.id))
        return response

    def entries(self, start = None, end = None):
        '''Retrieves entries from all people/tasks logged to this project.

        Can be filtered based on time by specifying start/end datetimes.'''
        if not start:
            start = self.earliest_record
        if not end:
            end = self.latest_record
        fr = start.strftime('%Y%m%d')
        to = end.strftime('%Y%m%d')
        url = str.format(
            'projects/{}/entries?from={}&to={}',
            self.id,
            fr,
            to,
        )
        response = self.hv.get_request(url)
        return [Entry(self.hv, ej['day_entry']) for ej in response]

    def task_assignments(self):
        '''Retrieves all tasks currently assigned to this project.'''
        url = str.format(
            'projects/{}/task_assignments',
            self.id
        )
        response = self.hv.get_request(url)
        return [TaskAssignment(self.hv, tj['task_assignment']) for tj in response]

class Client:
    '''A client in the Harvest system.'''
    def __init__(self, hv, json):
        self.hv = hv
        self.name = json['name'].encode('utf-8')
        self.id = json['id']
        self.created = parse_time(json['created_at'])
        self.updated = parse_time(json['updated_at'])
        self.highrise_id = json['highrise_id']
        self.cache_version = json['cache_version']
        self.currency = json['currency']
        self.currency_symbol = json['currency_symbol']
        self.active = json['active']
        self.details = json['details'].encode('utf-8')
        timeframes = json['default_invoice_timeframe']
        if timeframes and timeframes != 'Custom':
            pst = lambda timestr: \
                datetime.datetime.strptime(timestr, '%Y%m%d')
            self.invoice_timeframe = \
                map(pst, timeframes.split(','))
        else:
            self.invoice_timeframe = None
        self.last_invoice_kind = json['last_invoice_kind']

class Task:
    '''A Task in the Harvest system.'''
    def __init__(self, hv, json):
        self.default_billable = json['billable_by_default']
        self.deactivated = json['deactivated']
        self.default_hourly_rate = json['default_hourly_rate']
        self.id = json['id']
        self.name = json['name']
        self.default = json['is_default']
        self.updated = parse_time(json['updated_at'])
        self.created = parse_time(json['created_at'])

class TaskAssignment:
    '''A Task assigned to a Project.'''
    def __init__(self, hv, json):
        self.billable = json['billable']
        self.deactivated = json['deactivated']
        self.hourly_rate = json['hourly_rate']
        self.id = json['id']
        self.task_id = json['task_id']
        self.project_id = json['project_id']
        self.updated = parse_time(json['updated_at'])
        self.created = parse_time(json['created_at'])

