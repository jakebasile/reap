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

from setuptools import setup, find_packages

setup(
    name = 'reap',
    version = '0.7',
    description = 'A command line interface and library for the Harvest time tracking tool.',
    author = 'Jake Basile',
    author_email = 'jakebasile@me.com',
    url = 'https://github.com/jakebasile/reap/',
    download_url='https://github.com/downloads/jakebasile/reap/reap-0.7.tar.gz',
    packages = ['reap'],
    package_data = {
        '': ['README.md','LICENSE.txt','NOTICE.txt',]
    },
    scripts = [
        'reap/reap',
        'reap/reap-admin',
        'reap/reap-reports',
    ],
    install_requires = ['keyring'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Office/Business',
        'Topic :: Utilities',
    ],
)
