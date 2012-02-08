# Reap. The Simple Command Line for Harvest.

Reap focuses on providing a simple and clear command line interface to the [Harvest](http://www.harvestapp.com) time tracking system. It does not necessarily provide as in-depth an experience as [HCL](https://github.com/zenhob/hcl), but should serve most people's needs.

## Installation

**NOTE**: Reap will current *NOT* work in virtualenv, due to an issue in the upstream dependency [keyring](http://pypi.python.org/pypi/keyring).

    sudo pip install hg+http://code.jakebasile.com/reap

## Usage

The installation will add a new command to your system, `reap`. This will allow access to all of Reap's functionality.

To use Reap, you must first login. To do so, use the `login` command.

    reap login username password subdomain

To explore Reap's commands, try:

    reap -h

and for more information on other commands, try, for example:

    reap status -h

## More Help

If you can't figure something out, or you think Reap is broken, send me an [email](http://www.google.com/recaptcha/mailhide/d?k=01Setbc2JX7fNIQvHb-xyRqA==&c=J27oPGH6BTxbJKfL2FXzDSIGtNL1BzvC4Xt4Jomxcss=).
