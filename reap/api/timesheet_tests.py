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

import unittest
import random
import string
import datetime
from reap.api.timesheet import *

def random_string(length = 5):
    return ''.join(random.choice(string.ascii_lowercase) for x in xrange(length))

class TimesheetTest(unittest.TestCase):
    def setUp(self):
        # You need to have valid account info in an info.txt file to run tests.
        with open('info.txt') as info:
            self.base_uri = info.readline().strip()
            self.username = info.readline().strip()
            self.password = info.readline().strip()
        self.ts = Timesheet(self.base_uri, self.username, self.password)

class TestTimesheetLogin(TimesheetTest):
    def runTest(self):
        ts = Timesheet(self.base_uri, self.username, self.password)
        self.assertIsNotNone(ts)
        self.assertIsNotNone(ts.id)
        self.assertRaises(ValueError, Timesheet, random_string(), random_string(), random_string())

class TestProjectTask(TimesheetTest):
    def test_get_projects(self):
        projs = self.ts.projects()
        self.assertIsNotNone(projs)
        self.assertTrue(len(projs) > 0)
        for proj in projs:
            self.assertIsNotNone(proj.name)
            self.assertIsNotNone(proj.client)
            self.assertIsNotNone(proj.id)

    def test_get_tasks(self):
        projs = self.ts.projects()
        for proj in projs:
            tasks = proj.tasks()
            self.assertIsNotNone(tasks)
            self.assertTrue(len(tasks) > 0)
            for task in tasks:
                self.assertEqual(task.project.id, proj.id)
                self.assertIsNotNone(task.name)
                self.assertIsNotNone(task.id)
                self.assertIsNotNone(task.billable)

class TestEntry(TimesheetTest):
    def test_get(self):
        entries = self.ts.entries()
        self.assertIsNotNone(entries)
        for entry in entries:
            self.assertIsNotNone(entry.id)
            self.assertIsNotNone(entry.spent_at)
            self.assertIsNotNone(entry.user_id)
            self.assertIsNotNone(entry.client_name)
            self.assertIsNotNone(entry.project_id)
            self.assertIsNotNone(entry.project_name)
            self.assertIsNotNone(entry.task_id)
            self.assertIsNotNone(entry.task_name)
            self.assertIsNotNone(entry.hours)
            self.assertIsNotNone(entry.notes)
            if entry.started:
                self.assertIsNotNone(entry.timer_started)
                self.assertIsNotNone(entry.timer_created)
                self.assertIsNotNone(entry.timer_updated)

    def test_create(self):
        project = self.ts.projects()[0]
        task = project.tasks()[0]
        entry = self.ts.create_entry(project.id, task.id)
        self.assertIsNotNone(entry)
        self.assertTrue(entry.started)
        self.assertEqual(entry.project_id, project.id)
        self.assertTrue((entry.timer_created - datetime.datetime.utcnow()) < datetime.timedelta(minutes = 1))
        # clean up
        entry.delete()

    def test_delete(self):
        entries_count = len(self.ts.entries())
        project = self.ts.projects()[0]
        task = project.tasks()[0]
        entry = self.ts.create_entry(project.id, task.id)
        self.assertEqual(entries_count + 1, len(self.ts.entries()))
        entry.delete()
        self.assertEqual(entries_count, len(self.ts.entries()))

    def test_update_notes(self):
        project = self.ts.projects()[0]
        task = project.tasks()[0]
        entry = self.ts.create_entry(project.id, task.id)
        orig_notes = entry.notes
        new_note = random_string()
        entry.update(notes = new_note)
        self.assertEqual(new_note, entry.notes)
        # make sure it propagated to the server.
        new_entry = None
        for test_entry in self.ts.entries():
            if entry.id == test_entry.id:
                new_entry = test_entry
        self.assertIsNotNone(new_entry)
        self.assertEqual(new_entry.notes, new_note)
        entry.delete()

    def test_update_hours(self):
        project = self.ts.projects()[0]
        task = project.tasks()[0]
        entry = self.ts.create_entry(project.id, task.id)
        orig_hours = entry.hours
        new_hours = random.randint(0, 23)
        entry.update(hours = new_hours)
        self.assertEqual(new_hours, entry.hours)
        # make sure it propagated to the server.
        new_entry = None
        for test_entry in self.ts.entries():
            if entry.id == test_entry.id:
                new_entry = test_entry
        self.assertIsNotNone(new_entry)
        self.assertEqual(new_entry.hours, new_hours)
        entry.delete()

    def test_update_project(self):
        projects = self.ts.projects()
        project = projects[0]
        task = project.tasks()[0]
        new_proj = projects[1]
        new_task = new_proj.tasks()[0]
        entry = self.ts.create_entry(project.id, task.id)
        entry.update(project_id = new_proj.id, task_id = new_task.id)
        self.assertEqual(new_proj.id, entry.project_id)
        self.assertEqual(new_proj.name, entry.project_name)
        self.assertEqual(new_task.id, entry.task_id)
        self.assertEqual(new_task.name, entry.task_name)
        # make sure it propagated to the server.
        new_entry = None
        for test_entry in self.ts.entries():
            if entry.id == test_entry.id:
                new_entry = test_entry
        self.assertIsNotNone(new_entry)
        self.assertEqual(new_entry.project_id, new_proj.id)
        self.assertEqual(new_entry.task_id, new_task.id)
        entry.delete()

    def test_timer(self):
        project = self.ts.projects()[0]
        task = project.tasks()[0]
        entry = self.ts.create_entry(project.id, task.id)
        # it starts out running after creation.
        self.assertTrue(entry.started)
        entry.stop()
        self.assertFalse(entry.started)
        # make sure it propagated to the server.
        new_entry = None
        for test_entry in self.ts.entries():
            if entry.id == test_entry.id:
                new_entry = test_entry
        self.assertIsNotNone(new_entry)
        self.assertFalse(new_entry.started)
        # start it again.
        entry.start()
        self.assertTrue(entry.started)
        # make sure it propagated to the server.
        new_entry = None
        for test_entry in self.ts.entries():
            if entry.id == test_entry.id:
                new_entry = test_entry
        self.assertIsNotNone(new_entry)
        self.assertTrue(new_entry.started)
        entry.delete()


if __name__ == '__main__':
    unittest.main()
