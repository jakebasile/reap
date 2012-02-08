from setuptools import setup

setup(
    name = 'reap',
    version = '0.1',
    description = 'A command line interface for the Harvest time tracking tool.',
    author = 'Jake Basile',
    author_email = 'jakebasile@me.com',
    url = 'https://bitbucket.org/jakebasile/reap',
    scripts = ['src/reap'],
    install_requires = ['keyring'],
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
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
