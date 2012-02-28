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
import datetime

def parse_time(timestr):
    return datetime.datetime.strptime(timestr, '%Y-%m-%dT%H:%M:%SZ')

class ReapBase:
    def __init_request(self, path):
        auth = base64.b64encode(self.username + ':' + self.password)
        uri = self.base_uri + path
        request = urllib2.Request(uri)
        request.add_header('Content-Type', 'application/json')
        request.add_header('Accept', 'application/json')
        request.add_header('Authorization', 'Basic ' + auth)
        request.add_header('User-Agent', 'reap')
        return request

    def get_request(self, path):
        request = self.__init_request(path)
        try:
            result = urllib2.urlopen(request)
            result_json = json.load(result)
            return result_json
        except:
            return None

    def post_request(self, path, data, follow = False):
        request = self.__init_request(path)
        try:
            request.add_data(json.dumps(data))
            result = urllib2.urlopen(request)
            if result.code == 201 and follow:
                return self.get_request(result.headers.getheader('Location')[1:])
            result_json = json.load(result)
            return result_json
        except:
            return None

    def delete_request(self, path):
        request = self.__init_request(path)
        request.get_method = lambda: 'DELETE'
        try:
            result = urllib2.urlopen(request)
            if result:
                return True
            else:
                return False
        except:
            return None
