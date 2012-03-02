# **Reap**. The Simple Command Line for Harvest.

**Reap** focuses on providing a simple and clear command line interface to the [Harvest](http://www.harvestapp.com) time tracking system.

## Installation

To install the latest released version of **Reap**, use Pip:

    :::bash
    $ sudo pip install reap

## Usage

The installation will add a new command to your system, `reap`. This will allow access to all of **Reap**'s functionality.

### Login

To use **Reap**, you must first login. To do so, use the `login` command.

    :::bash
    $ reap login baseuri username

Where `baseuri` is the full base domain you log in to Harvest with, such as "https://companyname.harvestapp.com/". Your username is the email address you registered with. You will be asked for your password while this command executes.

### Help

To explore **Reap**'s commands, try:

    :::bash
    $ reap -h

and for more information on other commands, try, for example:

    :::bash
    $ reap status -h

### Working With Entries

*NOTE*: In previous versions of **Reap**, you specified and bookmarked _tasks_, now you work with the actual _entries_.

To add an entry to your time sheet, you will need to have project and task IDs you wish to associate with the entry. You can have **Reap** show you this information:

    :::bash
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

    :::bash
    $ reap create 1929052 1244476 -n 'Maui!' -t 5:20
    # Added entry:
    Project:    Internal
    Task:       Vacation
    ID:         74563731
    Notes:      Maui!
    Time:       5:20

You then work with the ID value for further commands, such as updating an entry:

    :::bash
    $ reap update 74563731 -t 2:15 -n 'Cleaned the stables.' -k 1929052 1244473
    # Updated entry:
    Project:    Internal
    Task:       Admin
    ID:         74565371
    Notes:      Cleaned the stables.
    Time:       2:15

Or starting a timer:

    :::bash
    $ reap start 74563731
    Entry timer started.

Or deleting an entry:

    :::bash
    $ reap delete 74563731
    Entry deleted.

For now, you need to specify the entry ID with all of these operations, the old regular expression search is gone until I figure out what to do with it.

## Administration

**Reap** now includes the beginnings of a basic administrative interface, under the `reap-admin` command. It currently supports the following operations:

* People
    * List
    * Create
    * Delete
* Projects
    * List
    * Create
    * Delete
* Clients
    * List

For example, the following command creates a new administrative user named "Mean Guy" in the department of Firings, with the email meanguy@example.com and the hourly rate of $150.00:

    :::bash
    $ reap-admin create-person -a -d 'Firings Department' -r 150.00 Mean Guy meanguy@example.com
    # Created person:
    Name:           Mean Guy
    ID:             315700
    Department:     Firings Department
    Admin:          True
    Contractor:     False
    Rate:           150.0

You can similarly delete users with the `delete-person` command:

    :::bash
    $ reap-admin delete-person 315700
    Person deleted.

For more information, run `reap-admin -h`.

## Reporting

**Reap** also includes some basic reporting functionality, under the `reap-admin` command. There is currently one report, `hours-report`. It shows the total, billable, and non-billable hour count for any number of people over a given time period. To generate this report over the course of a week, you would issue this command:

    :::bash
    $ reap-admin hours-report -s 20120227 -e 20120302 315700 315701 315702...
    # Hours Report for 20120227 - 20120302
    Name:           Mean Guy
    ID:             315700
    Total Hours:    11.0
    Billable:       6.0
    Non-billable:   5.0
    Ratio B/NB:     1.2
    % Billable:     54.55%
    ... and so on ...

## API

All of the meaty goodness of **Reap** is exposed in the API. The basic timesheet functions are available in the `reap.api.timesheet` module, while the advanced administrative code is in `reap.api.admin`. There is currently little documentation, but reading the rests in `reap.api.admin_tests` and `reap.api.timesheet_tests` and the actual commands may prove useful until more documentation is added.

A quick example of using the api is getting all projects that the current user is part of:

    :::python
    from reap.api.timesheet import Timesheet
    
    baseuri = 'https://yourcompany.harvestapp.com/'
    username = 'user'
    password = 'pa55w0rd'
    # Connects to Harvest and verifies UN/PW
    ts = Timesheet(baseuri, username, password)
    for project in ts.projects():
        print project.name


## More Help

If you can't figure something out, or you think **Reap** is broken, send me an [email](http://www.google.com/recaptcha/mailhide/d?k=01Setbc2JX7fNIQvHb-xyRqA==&c=J27oPGH6BTxbJKfL2FXzDSIGtNL1BzvC4Xt4Jomxcss=) or message me through Bitbucket.

## Future Plans

In the future, I plan to:

* Make working with entries easier.
* Add more error checking and more useful error messages.
* Add more administrative functions.

## Changelog

### v0.4

* Added input checking to IDs.
* Added reap-admin script for administrative functions.
* Added create-people to reap-admin.
* Added list-people to reap-admin.
* Added delete-person to reap-admin.
* Added list-clients to reap-admin.
* Added list-projects to reap-admin.
* Added hours-report to reap-admin.
* Added API support for projects, clients, people, and people's entries.
* Changed API to not require querying before creating an object.

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
