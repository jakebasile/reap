# Reap. The Simple Command Line for Harvest.

Reap focuses on providing a simple and clear command line interface to the [Harvest](http://www.harvestapp.com) time tracking system.

## Installation

**NOTE**: Reap will currently *NOT* work in virtualenv on at least OS X, due to an issue in the upstream dependency [keyring](http://pypi.python.org/pypi/keyring). A patch has been submitted to fix the problem.

To install the latest released version of Reap, use Pip:

    $ sudo pip install reap

## Usage

The installation will add a new command to your system, `reap`. This will allow access to all of Reap's functionality.

### Login

To use Reap, you must first login. To do so, use the `login` command.

    $ reap login baseuri username

Where `baseuri` is the full base domain you log in to Harvest with, such as "https://companyname.harvestapp.com/". Your username is the email address you registered with. You will be asked for your password while this command executes.

### Help

To explore Reap's commands, try:

    $ reap -h

and for more information on other commands, try, for example:

    $ reap status -h

### Working With Entries

*NOTE*: In previous versions of Reap, you specified and bookmarked _tasks_, now you work with the actual _entries_.

To add an entry to your time sheet, you will need to have project and task IDs you wish to associate with the entry. You can have Reap show you this information:

    $ reap list
    # Projects and Tasks:
    Internal
    |----Admin (1929052 1244473)
    |----Business Development (1929052 1244475)
    |----Project Management (1929052 1244474)
    |----Vacation (1929052 1244476)

    Test Project
    |----Admin (1929054 1244473)
    |----Project Management (1929054 1244474)

You then use those numbers in parenthesis, in that order, with the create command. You can optionally specify notes or hours already worked.

    $ reap create 1929052 1244476 -n 'Maui!' -t 5:80
    # Added entry:
    Project:    Internal
    Task:       Vacation
    ID:         74563731
    Notes:      Maui!
    Time:       6:19

You then work with the ID value for further commands, such as updating an entry:

    $ reap update 74563731 -t 2:15 -n 'Cleaned the stables.' -k 1929052 1244473
    # Updated entry:
    Project:    Internal
    Task:       Admin
    ID:         74565371
    Notes:      Cleaned the stables.
    Time:       2:15

Or starting a timer:

    $ reap start 74563731
    Entry timer started.

Or deleting an entry:

    $ reap delete 74563731
    Entry deleted.

For now, you need to specify the entry ID with all of these operations, the old regular expression search is gone until I figure out what to do with it.

## More Help

If you can't figure something out, or you think Reap is broken, send me an [email](http://www.google.com/recaptcha/mailhide/d?k=01Setbc2JX7fNIQvHb-xyRqA==&c=J27oPGH6BTxbJKfL2FXzDSIGtNL1BzvC4Xt4Jomxcss=).

## Future Plans

In the future, I plan to add:

* Make working with entries easier.
* More error checking and more useful error messages.
* Combined command capabilities, so that you can start a task and add a note to that task in one go.

## Changelog

### v0.3

* Rewrote the entire backend.
* Shifted focus from tasks to entries.
* Added create command.
* Added list command.
* Changed how Status prints data.
* Changed login params. Shouldn't break against existing logins.
* Removed bookmarks until I can figure out if they work with new Entries focus.

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
