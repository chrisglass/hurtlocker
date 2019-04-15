import os
import sys
import subprocess

# This should be configuration
USERNAME="CHANGEME"  # Your unix username
XAUTHORITY_FILE=os.path.join("/home", USERNAME, ".Xauthority")
DISPLAY=":0"  # Tricky if the user is running on another display.

def locked():
    # Is the current account locked?
    lines = []
    with open("/etc/shadow", "r") as shadow:
        lines = shadow.readlines()

    for line in lines:
        if line.startswith(USERNAME):
            # Get the first character of the first split after ":" for the
            # interesting username. If it's a "!", then it is locked.
            locked=line.split(":")[1][0]
            return locked == "!"

    # In any other case, return True (if unsure, don't lock someone :)
    return True


def unlock_session():
    print("Unlocking " + USERNAME)
    subprocess.run("/usr/bin/usermod -U " + USERNAME, shell=True)


def lock_session():
    """Lock the session down for the user in question (works on i3)."""
    print("Locking " + USERNAME)
    env = {"XAUTHORITY": XAUTHORITY_FILE,
           "DISPLAY": DISPLAY}
    subprocess.run("/usr/sbin/usermod -L " + USERNAME, shell=True)
    subprocess.run("sudo -u " + USERNAME + " /usr/bin/i3lock --color=000000",
                   shell=True, env=env)
