# **Reap**. The Simple Command Line for Harvest.

**Reap** focuses on providing a simple and clear command line interface to the [Harvest](http://www.harvestapp.com) time tracking system.

## Installation

To install the latest released version of **Reap**, use Pip:

    $ sudo pip install reap

## Timesheet

The installation will add a new command to your system, `reap`. This will allow access to all of **Reap**'s personal timesheet functionality.

### Login

To use **Reap**, you must first login. To do so, use the `login` command.

    $ reap login baseuri username

Where `baseuri` is the full base domain you log in to Harvest with, such as "https://companyname.harvestapp.com/". Your username is the email address you registered with. You will be asked for your password while this command executes.

### Help

To explore **Reap**'s commands, try:

    $ reap -h

and for more information on other commands, try, for example:

    $ reap status -h

### Working With Entries

To add an entry to your time sheet, you will need to have project and task IDs you wish to associate with the entry. You can have **Reap** show you this information:

    $ reap list
    Projects and Tasks:
        - Test Project 1:
            - Admin (1966498 1244473)
            - Project Management (1966498 1244474)
    
        - Test Project 2:
            - Admin (1966708 1244473)
            - Project Management (1966708 1244474)
    
        - Test Project 3:
            - Admin (1981495 1244473)
            - Project Management (1981495 1244474)

You then use those numbers in parenthesis, in that order, with the create command. You can optionally specify notes or hours already worked.

    $ reap create 1966498 1244474 -n 'TPS Reports' -t 5:20
    Added Entry:
        Project:    Test Project 1
        Task:       Project Management
        ID:         77509008
        Notes:      TPS Reports
        Time:       5:19

You can then work with the ID value for further commands, such as updating an entry:

    $ reap update 77509008 -t 2:15 -n 'Met with the Bobs.' -k 1966498 1244473
    Updated Entry:
        Project:    Test Project 1
        Task:       Admin
        ID:         77509008
        Notes:      Met with the Bobs.
        Time:       2:15

Or starting a timer:

    $ reap start 77509008
    Entry timer started.

Or deleting an entry:

    $ reap delete 77509008
    Entry deleted.

As of **Reap** 0.5, you can also specify what entry you are working with by using all or part of the Task name for that entry. So for the above examples you could use 'admin', 'Admin', 'ad.*', and so on instead of the ID 77509008.


## Administration

**Reap** includes a basic administrative interface, under the `reap-admin` command. It currently supports the following operations:

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

    $ reap-admin create-person -a -d 'Firings Department' -r 150.00 Mean Guy meanguy@example.com
    Created Person:
            Name:           Mean Guy
            ID:             320171
            Department:     Firings Department
            Admin:          True
            Contractor:     False
            Rate:           150.0

You can similarly delete users with the `delete-person` command:

    $ reap-admin delete-person 320171
    Person deleted.

For more information, run `reap-admin -h`.

## Reporting

**Reap** also includes some basic reporting functionality, under the `reap-reports` command. An example is the `hours` report: it shows the total, billable, and non-billable hour count for any number of people over a given time period. To generate this report over the course of a week, you would issue this command:

    $ reap-reports hours -s 20120227 -e 20120302 315700 315701 315702...
    Hours Report:
        From: 2012-02-27
        To: 2012-03-02
        Results:
        -   Name:           Mean Guy
            ID:             315700
            Total Hours:    11.0
            Billable:       6.0
            Non-billable:   5.0
            Ratio B/NB:     1.2
            % Billable:     54.55%
    ... and so on ...

There is also a `projects` report that lists the projects a person has worked on over a given time period along with the hours logged to that project, a `tasks` report that lists the tasks a user has worked on across projects over a given time period, and a `tasks-by-projects` report that displays all tasks logged by all people to a given project.

## API

All of the meaty goodness of **Reap** is exposed in the API. The basic timesheet functions are available in the `reap.api.timesheet` module, while the advanced administrative code is in `reap.api.admin`. There is currently little documentation, but reading the rests in `reap.api.admin_tests` and `reap.api.timesheet_tests` and the actual commands may prove useful until more documentation is added.

A quick example of using the api is getting all projects that the current user is part of:

    from reap.api.timesheet import Timesheet
    
    baseuri = 'https://yourcompany.harvestapp.com/'
    username = 'user'
    password = 'pa55w0rd'
    # Connects to Harvest and verifies UN/PW
    ts = Timesheet(baseuri, username, password)
    for project in ts.projects():
        print project.name


## More Help

If you can't figure something out, check the [issue tracker](https://github.com/jakebasile/reap/issues), and I'll look into it as soon as I can.

## Future Plans

In the future, I plan to:

* Add more error checking and more useful error messages.
* Add more administrative functions.

## Changelog

### v0.6

* Moved everything to GitHub!

### v0.5

* Added tasks-by-project report to reap-reports.
* Fixed reap list output.
* Added in simple regex task name matching.

### v0.4

* Moved all output to YAML compatible format.
* Added input checking to IDs.
* Added reap-admin script for administrative functions.
* Added create-people to reap-admin.
* Added list-people to reap-admin.
* Added delete-person to reap-admin.
* Added list-clients to reap-admin.
* Added list-projects to reap-admin.
* Added hours report to reap-reports.
* Added projects report to reap-reports.
* Added tasks report to reap-reports
* Added API support for projects and project's entries
* Added API support for clients
* Added API support for people and people's entries
* Added API support for tasks
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
