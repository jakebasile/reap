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

import unittest
import random
import string
import datetime
from reap.api.admin import *

def random_string(length = 5):
    return ''.join(random.choice(string.ascii_lowercase) for x in xrange(length))

class HarvestTest(unittest.TestCase):
    def setUp(self):
        # You need to have valid account info in an info.txt file to run tests.
        with open('info.txt') as info:
            self.base_uri = info.readline().strip()
            self.username = info.readline().strip()
            self.password = info.readline().strip()
        self.hv = Harvest(self.base_uri, self.username, self.password)

class TestHarvestLogin(HarvestTest):
    def runTest(self):
        hv = Harvest(self.base_uri, self.username, self.password)
        self.assertIsNotNone(hv)
        self.assertRaises(ValueError, Harvest, random_string(), random_string(), random_string())

class TestPeople(HarvestTest):
    def test_get(self):
        people = self.hv.people()
        self.assertIsNotNone(people)
        for person in people:
            self.assertIsNotNone(person)
            self.assertIsNotNone(person.id)
            self.assertIsNotNone(person.email)
            self.assertIsNotNone(person.first_name)
            self.assertIsNotNone(person.last_name)
            self.assertIsNotNone(person.all_future)
            self.assertIsNotNone(person.active)
            self.assertIsNotNone(person.admin)
            self.assertIsNotNone(person.contractor)
            self.assertIsNotNone(person.telephone)
            self.assertIsNotNone(person.timezone)
            # optional ones
            # self.assertIsNotNone(person.department)
            # self.assertIsNotNone(person.default_rate)

    def test_create(self):
        fn = random_string()
        ln = random_string()
        email = random_string() + '@example.com'
        contractor = bool(random.getrandbits(1))
        admin = bool(random.getrandbits(1))
        department = random_string()
        default_rate = random.random() * 10
        person = self.hv.people().create(
            fn,
            ln,
            email,
            contractor = contractor,
            admin = admin,
            department = department,
            default_rate = default_rate,
        )
        self.assertIsNotNone(person)
        self.assertIsNotNone(person)
        self.assertIsNotNone(person.id)
        self.assertIsNotNone(person.email)
        self.assertEqual(person.email, email)
        self.assertIsNotNone(person.first_name)
        self.assertEqual(person.first_name, fn)
        self.assertIsNotNone(person.last_name)
        self.assertEqual(person.last_name, ln)
        self.assertIsNotNone(person.all_future)
        self.assertIsNotNone(person.active)
        self.assertIsNotNone(person.admin)
        self.assertEqual(person.admin, admin)
        self.assertIsNotNone(person.contractor)
        self.assertEqual(person.contractor, contractor)
        self.assertIsNotNone(person.telephone)
        self.assertIsNotNone(person.timezone)
        # clean up
        person.delete()

    def test_delete(self):
        person = self.hv.people().create(
            random_string(),
            random_string(),
            random_string() + '@example.com',
        )
        self.assertIsNotNone(person)
        id = person.id
        person.delete()
        # ensure it's no longer there.
        for p in self.hv.people():
            if p.id == id:
                self.fail()

class TestProjects(HarvestTest):
    def test_get(self):
        projects = self.hv.projects()
        self.assertIsNotNone(projects)
        for project in projects:
            self.assertIsNotNone(project.id)
            self.assertIsNotNone(project.name)
            self.assertIsNotNone(project.active)
            self.assertIsNotNone(project.billable)
            self.assertIsNotNone(project.bill_by)
            self.assertTrue(hasattr(project, 'hourly_rate'))
            self.assertIsNotNone(project.client_id)
            self.assertTrue(hasattr(project, 'code'))
            self.assertTrue(hasattr(project, 'notes'))
            self.assertIsNotNone(project.budget_by)
            self.assertTrue(hasattr(project, 'budget'))
            self.assertIsNotNone(project.latest_record)
            self.assertIsNotNone(project.earliest_record)
            self.assertIsNotNone(project.updated)
            self.assertIsNotNone(project.created)


if __name__ == '__main__':
    unittest.main()