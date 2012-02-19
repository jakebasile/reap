# Reap. The Simple Command Line for Harvest.

Reap focuses on providing a simple and clear command line interface to the [Harvest](http://www.harvestapp.com) time tracking system.

## Installation

**NOTE**: Reap will currently *NOT* work in virtualenv, due to an issue in the upstream dependency [keyring](http://pypi.python.org/pypi/keyring).

To install the latest released version of Reap, use Pip:

    sudo pip install reap

## Usage

The installation will add a new command to your system, `reap`. This will allow access to all of Reap's functionality.

### Login

To use Reap, you must first login. To do so, use the `login` command.

    reap login baseuri username

Where `baseuri` is the full base domain you log in to Harvest with, such as "https://companyname.harvestapp.com/". Your username is the email address you registered with. You will be asked for your password while this command executes.

### Help

To explore Reap's commands, try:

    reap -h

and for more information on other commands, try, for example:

    reap status -h

### Specifying Tasks

To specify a task, you can specify all or part of the task name. For instance, to start a timer on a task named "Software Engineering", you can use any of the following:

    reap start 'software engineering'
    reap start soft
    reap start eng
    reap start '.*Engineering'

If there are multiple tasks that match the task query entered, such as if two projects have "Software Engineering", you will be presented with a list to select from. To save time, you can create a bookmark to the task's project ID and task ID using `bookmark`. Then you can use the bookmark anywhere Reap expects a task name.

## More Help

If you can't figure something out, or you think Reap is broken, send me an [email](http://www.google.com/recaptcha/mailhide/d?k=01Setbc2JX7fNIQvHb-xyRqA==&c=J27oPGH6BTxbJKfL2FXzDSIGtNL1BzvC4Xt4Jomxcss=).

## Future Plans

In the future, I plan to add:

* A whole bunch more error checking and more useful error messages.
* Combined command capabilities, so that you can start a task and add a note to that task in one go.
* General code cleanup. I wrote most of this in two weeknights, so there's room for improvement.
* A way to view all available projects and tasks.
* Better bookmarking.

## Changelog

### v0.2

* Moved to a better password entry mechanism.
* Changed time output to hours:minutes.
* Added user-agent to all requests.
* Added daily total time to status message.

### v0.1.2

* Changed setup.py to enable simple download from Pip, PyPI.

### v0.1.1

* fixed an issue arising from moving to different files.

### v0.1

* Initial Release!
