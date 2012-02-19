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
from reap.api import *

def random_string(length = 5):
    return ''.join(random.choice(string.ascii_lowercase) for x in xrange(length))

class ReapTest(unittest.TestCase):
    def setUp(self):
        # You need to have valid account info in an info.txt file to run tests.
        with open('info.txt') as info:
            self.base_uri = info.readline().strip()
            self.username = info.readline().strip()
            self.password = info.readline().strip()
            self.ts = Timesheet(self.base_uri, self.username, self.password)

class TestLogin(ReapTest):
    def runTest(self):
        ts = Timesheet(self.base_uri, self.username, self.password)
        self.assertIsNotNone(ts)
        self.assertRaises(ValueError, Timesheet, random_string(), random_string(), random_string())

class TestProjectTask(ReapTest):
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
                self.assertIsNotNone(task.name)
                self.assertIsNotNone(task.id)
                self.assertIsNotNone(task.billable)

class TestEntry(ReapTest):
    def test_get_entries(self):
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


if __name__ == '__main__':
    unittest.main()