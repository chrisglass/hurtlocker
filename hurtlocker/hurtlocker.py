import datetime
import os
import sys

from hurtlocker.strava import should_unlock
from hurtlocker.i3lock import locked, unlock_session, lock_session


__version__ = "0.0.1"


#TODO: Most of these things should be configuration really
LOCK_TIME_OF_DAY=datetime.time(hour=12, minute=00)


def should_lock():
    """Lock the computer if now is later than the configured lock time."""
    if should_unlock(LOCK_TIME_OF_DAY):
        # No need to lock anymore, we've already unlocked once today.
        return False

    now = datetime.datetime.now().time()
    # This naive test ensures that we automatically unlock at midnight.
    if now >= LOCK_TIME_OF_DAY:
        return True
    return False



def main():

    if os.geteuid() != 0:
        print("Hurtlocker needs to be run as root.")
        sys.exit(1)

    if locked():
        if should_unlock(LOCK_TIME_OF_DAY):
            unlock_session()
    else:
        if should_lock():
            lock_session()
