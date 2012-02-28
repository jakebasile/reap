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
from reap.commands.support import *

PERSON_FORMAT = '''Name:           {person.first_name} {person.last_name}
ID:             {person.id}
Department:     {person.department}
Admin:          {person.admin}
Contractor:     {person.contractor}
Rate:           {person.default_rate}
'''

def get_harvest():
    info = load_info()
    if info:
        base_uri = info[0]
        username = info[1]
        passwd = keyring.get_password(base_uri, username)
        return reap.api.admin.Harvest(base_uri, username, passwd)

def list_people(args):
    hv = get_harvest()
    if hv:
        contractors = []
        employees = []
        for person in hv.people():
            if person.contractor:
                contractors += [person]
            else:
                employees += [person]
        if len(employees) > 0:
            print '# Employees'
            for emp in employees:
                print str.format(PERSON_FORMAT, person = emp)
        if len(contractors) > 0:
            print '# Contractors'
            for contractor in contractors:
                print str.format(PERSON_FORMAT, person = contractor)

def create_person(args):
    hv = get_harvest()
    if hv:
        person = hv.people().create(
            args.firstname,
            args.lastname,
            args.email,
            admin = args.admin or False,
            contractor = args.contractor or False,
            department = args.department,
            default_rate = float(args.rate),
        )
        if person:
            print '# Created person:'
            print str.format(
                PERSON_FORMAT,
                person = person,
            )
        else:
            print 'Could not create person.'

def delete_person(args):
    hv = get_harvest()
    if hv:
        id = int(args.personid)
        for person in hv.people():
            if person.id == int(id):
                person.delete()
                print 'Person deleted.'
                break

