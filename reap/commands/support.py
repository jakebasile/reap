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

import os.path

def save_info(base_uri, username):
    with open(os.path.expanduser('~/.reaprc'), 'w') as file:
        file.write(base_uri + '\n')
        file.write(username + '\n')

def load_info():
    if os.path.exists(os.path.expanduser('~/.reaprc')):
        with open(os.path.expanduser('~/.reaprc'), 'r') as file:
            base_uri = file.readline().strip()
            username = file.readline().strip()
            return (base_uri, username)
    else:
        print 'Please login first.'


