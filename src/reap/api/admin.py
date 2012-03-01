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

from reap.api.base import ReapBase, parse_time, parse_short_time

class Harvest(ReapBase):
    def __init__(self, base_uri, username, password):
        self.base_uri = base_uri
        self.username = username
        self.password = password
        login_response = self.get_request('account/who_am_i')
        if not login_response:
            raise ValueError('Unable to login with given info.')
        if not login_response['user']['admin']:
            raise ValueError('User is not an admin')

    def people(self):
        people_response = self.get_request('people/')
        return People(self, people_response)

    def projects(self):
        projects_response = self.get_request('projects/')
        return Projects(self, projects_response)

    def clients(self):
        clients_response = self.get_request('clients/')
        return Clients(self, clients_response)

    def create_person(self, first_name, last_name, email, department = None, default_rate = None, admin = False, contractor = False):
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

    def create_project(self, name, client_id, budget = None, budget_by = 'none', notes = None, billable = True):
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

class People:
    def __init__(self, hv, json):
        self.hv = hv
        self.people_list = [Person(hv, pjson['user']) for pjson in json]

    def __iter__(self):
        return iter(self.people_list)

    def __len__(self):
        return len(self.people_list)

class Person:
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
        response = self.hv.delete_request('people/' + str(self.id))
        return response

class Projects:
    def __init__(self, hv, json):
        self.hv = hv
        self.project_list = [Project(hv, pjson['project']) for pjson in json]

    def __iter__(self):
        return iter(self.project_list)

    def __len__(self):
        return len(self.project_list)

class Project:
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
        self.latest_record = parse_short_time(json['hint-latest-record-at'])
        self.earliest_record = parse_short_time(json['hint-earliest-record-at'])
        self.created = parse_time(json['created_at'])
        self.updated = parse_time(json['updated_at'])

    def delete(self):
        response = self.hv.delete_request('projects/' + str(self.id))
        return response

class Clients:
    def __init__(self, hv, json):
        self.hv = hv
        self.client_list = [Client(hv, cjson['client']) for cjson in json]

    def __iter__(self):
        return iter(self.client_list)

    def __len__(self):
        return len(self.client_list)

    def __getitem__(self, index):
        return self.client_list[index]

class Client:
    def __init__(self, hv, json):
        self.hv = hv
        self.name = json['name']
        self.id = json['id']
        self.created = parse_time(json['created_at'])
        self.updated = parse_time(json['updated_at'])
        self.highrise_id = json['highrise_id']
        self.cache_version = json['cache_version']
        self.currency = json['currency']
        self.currency_symbol = json['currency_symbol']
        self.active = json['active']
        self.details = json['details']
        timeframes = json['default_invoice_timeframe']
        if timeframes:
            self.invoice_timeframe = (
                parse_short_time(timeframes[0]),
                parse_short_times(timeframes[1])
            )
        else:
            self.invoice_timeframe = None
        self.last_invoice_kind = json['last_invoice_kind']
