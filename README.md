Hurtlocker
============

*A pretty bad idea*

Hurtlocker is an application that will lock your workstation, until you
successfully post a sport activity on [Strava](https://strava.com).

Usage
-----

**THIS WILL LOCK YOU OUT OF YOUR MACHINE IF YOU DONT SETUP A
SECOND ADMIN USER YOU CAN SWITCH TO**

(until you complete an activity, of course)

Grab the tree, then start a virtualenv, and activate it:

```bash
python3 -m venv .venv
source venv/bin/activate
pip install -r requirements.txt
```

- You need a strava account.
- This currently only works for i3vm (it invokes i3lock).
- You need to create an application at https://www.strava.com/settings/api
- Once you created your application, stick your `clientid` and `client secret` in
  the hurtlocker/hurtlocker.py script.
- Also stick your system-level username (for now, it's hardcoded as well) in there.
- Run the script AS ROOT with the aptly named `run.sh` script.

The first time you run the script it will initiate the painful OAUTH2 dance
and store your secrets in `.hurtlocker`.

The idea is that this script would be installed system-wide and then invoked in
a cron, periodically.


Once this is done, it will lock your screen using `i3lock`, and then ``IT WILL
LOCK YOUR SYSTEM USER!``

Unlocking
---------

To unlock your screen, you must first go out and register a strava activity,
then your password will be reactivated (your unix-level user's password will be
unlocked and you will be allowed to log back in).

Emergency unlock
---------------

What if you really want to use your computer for some super urgent matter?

Well, it's an alpha POC script. You're on your own, but it shouldn't be too hard
to setup a second user that you can switch to and unlock your password
manually using `sudo usermod -U <username>`

You're not trying to cheat... right?


