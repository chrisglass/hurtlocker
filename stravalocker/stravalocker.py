import datetime
import time
import subprocess
import sys


__version__ = "0.0.1"

# We lock at noon!
lock_time_of_day=datetime.time(hour=12, minute=00)

username="tribaal"

stava_token=""
strava_sport=""
strava_distance=""


def check_unlock_condition():
    # Query strava here.

    # FIXME: The poor sod, he'll never get anything done.
    return False


def check_lock_condition():
    """Lock the computer if now is later than the configured lock time."""
    now = datetime.datetime.now().time()
    # This naive test ensures that we automatically unlock at midnight.
    if now >= lock_time_of_day:
        return True
    return False


def locked():
    # Is the current account locked?
    lines = []
    with open("/etc/shadow", "r") as shadow:
        lines = shadow.readlines()

    for line in lines:
        if line.startswith(username):
            # Get the first character of the first split after ":" for the
            # interesting username. If it's a "!", then it is locked.
            locked=line.split(":")[1][0]
            return locked == "!"

    # In any other case, return True (if unsure, don't lock someone :)
    return True


def unlock_session():
    # unlock the poor dude
    print("Unlocking " + username)
    subprocess.run("/usr/bin/usermod -U " + username, shell=True)


def lock_session():
    """Lock the session down for the user in question (works on i3)."""
    print("Locking " + username)
    subprocess.run("/usr/sbin/usermod -L " + username, shell=True)
    subprocess.run("sudo -u " + username + " /usr/bin/i3lock --color=000000", shell=True)

def main():
    now = datetime.datetime.now().time()
    today_target = datetime.time(hour=14, minute=30)
    print(now)
    print(today_target)
    print(now > today_target)
    sys.exit(0)

    if locked():
        if check_unlock_condition():
            unlock_session()
    else:
        if check_lock_condition():
            lock_session()
