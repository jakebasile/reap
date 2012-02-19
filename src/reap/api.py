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

import urllib2
import json
import base64
import reap.constants

class Timesheet:
    def __init__(self, base_uri, username, password):
        self.base_uri = 'https://' + base_uri + '.harvestapp.com/'
        self.username = username
        self.password = password
        login_request = self.__get_request('account/who_am_i')
        login_response = self.__proc_request(login_request)
        if not login_response:
            raise ValueError('Unable to login with given info.')

    def __get_request(self, path):
        auth = base64.b64encode(self.username + ':' + self.password)
        uri = self.base_uri + path
        request = urllib2.Request(uri)
        request.add_header('Content-Type', 'application/json')
        request.add_header('Accept', 'application/json')
        request.add_header('Authorization', 'Basic ' + auth)
        request.add_header('User-Agent', 'reap')
        return request

    def __proc_request(self, req):
        result = urllib2.urlopen(req)
        result_json = json.load(result)
        return result_json
