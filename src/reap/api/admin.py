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

from reap.api.base import ReapBase, parse_time

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

class People:
    def __init__(self, hv, json):
        self.hv = hv
        self.people_list = [Person(hv, pjson['user']) for pjson in json]

    def __iter__(self):
        return iter(self.people_list)

    def __len__(self):
        return len(self.people_list)

    def create(self, first_name, last_name, email, department = None, default_rate = None, admin = False, contractor = False):
        person = {'user':{
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'department': department,
            'default_hourly_rate': default_rate,
            'is_admin': admin,
            'is_contractor': contractor,
        }}
        response = self.hv.post_request('people/', person, follow = True)
        if response:
            return Person(self.hv, response['user'])

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
