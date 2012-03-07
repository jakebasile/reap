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
from reap.api.timesheet import Timesheet

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
        self.assertIsNotNone(hv.id)
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
        person = self.hv.create_person(
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
        person = self.hv.create_person(
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

    def test_entries(self):
        # need to get a timesheet for the current user.
        ts = Timesheet(self.base_uri, self.username, self.password)
        # create some entries.
        projects = ts.projects()
        self.assertTrue(len(projects) > 0)
        entries = []
        for i in xrange(random.randint(0, 5)):
            project = random.choice(projects)
            task = random.choice(project.tasks())
            entry = ts.create_entry(project.id, task.id, hours = random.random() * 10)
            entry.stop()
            entries += [entry]
        # Get the entries from the admin interface.
        person = None
        for p in self.hv.people():
            if p.id == ts.id:
                person = p
        self.assertIsNotNone(person)
        report_entries = person.entries(
            start = datetime.datetime.today(),
            end = datetime.datetime.today(),
        )
        # ensure the data is there.
        for rentry in report_entries:
            self.assertIsNotNone(rentry.hours)
            self.assertIsNotNone(rentry.id)
            self.assertTrue(hasattr(rentry, 'notes'))
            self.assertIsNotNone(rentry.project_id)
            self.assertIsNotNone(rentry.task_id)
            self.assertIsNotNone(rentry.user_id)
            self.assertIsNotNone(rentry.billed)
            self.assertIsNotNone(rentry.closed)
            self.assertIsNotNone(rentry.updated)
            self.assertIsNotNone(rentry.created)
        # ensure the data matches up.
        self.assertEqual(len(report_entries), len(entries))
        matches = 0
        for rentry in report_entries:
            for oentry in entries:
                if oentry.id == rentry.id:
                    matches += 1
                    self.assertEqual(oentry.hours, rentry.hours)
                    self.assertEqual(oentry.project_id, rentry.project_id)
                    self.assertEqual(oentry.task_id, rentry.task_id)
                    break
        # Clean up
        for entry in entries:
            entry.delete()


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

    def test_create(self):
        name = random_string()
        budget_by = random.choice(Project.BUDGET_BY_TYPE)
        client_id = random.choice(self.hv.clients()).id
        notes = random_string()
        budget = round(random.random() * 100, 2)
        billable = bool(random.getrandbits(1))
        project = self.hv.create_project(
            name,
            client_id,
            budget = budget,
            budget_by = budget_by,
            notes = notes,
            billable = billable,
        )
        self.assertIsNotNone(project)
        self.assertEqual(project.name, name)
        self.assertEqual(project.client_id, client_id)
        self.assertEqual(project.budget, budget)
        self.assertEqual(project.budget_by, budget_by)
        self.assertEqual(project.notes, notes)
        self.assertEqual(project.billable, billable)
        # clean up
        project.delete()

    def test_delete(self):
        name = random_string()
        client_id = random.choice(self.hv.clients()).id
        project = self.hv.create_project(
            name,
            client_id,
        )
        self.assertIsNotNone(project)
        id = project.id
        project.delete()
        # ensure it's not on the server.
        for proj in self.hv.projects():
            if proj.id == id:
                self.fail()

    def test_entries(self):
        # create test entries.
        ts = Timesheet(self.base_uri, self.username, self.password)
        project = ts.projects()[0]
        tasks = project.tasks()
        self.assertIsNotNone(project)
        entries = []
        for i in xrange(random.randint(1, 5)):
            task = random.choice(tasks)
            entry = ts.create_entry(project.id, task.id, hours = random.random() * 10)
            entry.stop()
            entries += [entry]
        # get the entries from the project.
        for p in self.hv.projects():
            if p.id == project.id:
                admin_proj = p
        self.assertIsNotNone(admin_proj)
        proj_entries = admin_proj.entries(
            start = admin_proj.earliest_record,
            end = admin_proj.latest_record
        )
        # make sure the data exists.
        for proj_entry in proj_entries:
            self.assertIsNotNone(proj_entry.hours)
            self.assertIsNotNone(proj_entry.id)
            self.assertTrue(hasattr(proj_entry, 'notes'))
            self.assertIsNotNone(proj_entry.project_id)
            self.assertIsNotNone(proj_entry.task_id)
            self.assertIsNotNone(proj_entry.user_id)
            self.assertIsNotNone(proj_entry.billed)
            self.assertIsNotNone(proj_entry.closed)
            self.assertIsNotNone(proj_entry.updated)
            self.assertIsNotNone(proj_entry.created)
        # ensure that all entries created were found.
        for orig_entry in entries:
            found = False
            for proj_entry in proj_entries:
                if proj_entry.id == orig_entry.id:
                    found = True
                    break
            if not found:
                self.fail()
        # clean up
        for orig_entry in entries:
            orig_entry.delete()

class TestClients(HarvestTest):
    def test_get(self):
        clients = self.hv.clients()
        self.assertIsNotNone(clients)
        for client in clients:
            self.assertIsNotNone(client.name)
            self.assertIsNotNone(client.created)
            self.assertIsNotNone(client.updated)
            self.assertIsNotNone(client.id)
            self.assertTrue(hasattr(client, 'highrise_id'))
            self.assertIsNotNone(client.cache_version)
            self.assertIsNotNone(client.currency)
            self.assertIsNotNone(client.active)
            self.assertIsNotNone(client.currency_symbol)
            self.assertIsNotNone(client.details)
            self.assertTrue(hasattr(client, 'invoice_timeframe'))
            if client.invoice_timeframe:
                self.assertIsNotNone(client.invoice_timeframe[0])
                self.assertIsNotNone(client.invoice_timeframe[1])
            self.assertTrue(hasattr(client, 'last_invoice_kind'))

class TestTasks(HarvestTest):
    def test_get(self):
        tasks = self.hv.tasks()
        self.assertIsNotNone(tasks)
        for task in tasks:
            self.assertIsNotNone(task.default_billable)
            self.assertIsNotNone(task.deactivated)
            self.assertTrue(hasattr(task, 'default_hourly_rate'))
            self.assertIsNotNone(task.id)
            self.assertIsNotNone(task.default)
            self.assertIsNotNone(task.name)
            self.assertIsNotNone(task.updated)
            self.assertIsNotNone(task.created)


if __name__ == '__main__':
    unittest.main()
