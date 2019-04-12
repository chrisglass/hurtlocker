import datetime
import time
import subprocess
import sys
import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

from stravalib import Client

__version__ = "0.0.1"

#TODO: Most of these things should be configuration really
CLIENT_ID="REPLACEME"
CLIENT_SECRET="REPLACEME"
USERNAME="REPLACEME"  # Your unix username
LOCK_TIME_OF_DAY=datetime.time(hour=12, minute=00)


class PainfulHTTPServer(HTTPServer):
    """Python Y U do this to me.

    The default HTTPServer is not stoppable, probably to prevent people from
    doing something stupid such as this script. Ah well."""

    running = True

    def serve_until_stopped(self):
        # The normal HTTPServer is not stoppable. We don't actually want
        # to listen any longer than just enough to grab the redirect info
        # once the user authorized this app to get a token.
        while self.running:
            self.handle_request()

    def stop(self):
        self.running = False


class StravaOauthRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # when we are called with a GET we want to get the "code" from the
        # request string
        code=""
        splits=self.path.split("&")
        for s in splits:
            if s.startswith("code="):
                code=s.split("code=")[1]

        assert code

        # Let's just do the dirty and do the auth inline with the request...
        # It's not like we expect a lot of traffic anyway.
        client = Client()
        access_token = client.exchange_code_for_token(client_id=CLIENT_ID,
                                              client_secret=CLIENT_SECRET,
                                              code=code)

        with open(".hurtlocker", "w") as thefile:
            thefile.write(json.dumps(access_token))

        if access_token:
            self.server.stop()


def get_token_from_disk():
    """Get the saved token from disk, or return an empty string if there is none."""
    contents = ""
    if os.path.isfile(".hurtlocker"):
        with open(".hurtlocker", "r") as thefile:
            contents = thefile.read()

    if contents == "":
        return contents

    tokens = json.loads(contents)

    # TODO: handle the expiration case.
    return tokens["access_token"]


def get_strava_token():
    """Return a valid strava token.

    This will initiate the OAUTH dance if needed, or just get the token from disk."""

    if get_token_from_disk() == "":
        client = Client()
        url = client.authorization_url(client_id=CLIENT_ID,
                                       redirect_uri='http://127.0.0.1:5000/authorization')

        print("Please open this in your browser:" + url)

        server_address = ('', 5000)
        httpd = PainfulHTTPServer(server_address, StravaOauthRequestHandler)
        httpd.serve_until_stopped()

    # Now the file really shouldn't be empty anymore.
    token = get_token_from_disk()
    return token


def check_unlock_condition():
    """Determine whether the person registered an activity since lock time."""
    token = get_strava_token()
    client = Client(access_token=token)
    today = datetime.date.today()
    afterdate = datetime.datetime.combine(today, LOCK_TIME_OF_DAY)

    activities = client.get_activities(after=afterdate.isoformat())

    # Did the locked person record at least one activity since the lock time?
    if len(activites) > 0:
        return True
    return False


def check_lock_condition():
    """Lock the computer if now is later than the configured lock time."""
    now = datetime.datetime.now().time()
    # This naive test ensures that we automatically unlock at midnight.
    if now >= LOCK_TIME_OF_DAY:
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
    print("Unlocking " + username)
    subprocess.run("/usr/bin/usermod -U " + username, shell=True)


def lock_session():
    """Lock the session down for the user in question (works on i3)."""
    print("Locking " + username)
    subprocess.run("/usr/sbin/usermod -L " + username, shell=True)
    subprocess.run("sudo -u " + username + " /usr/bin/i3lock --color=000000",
                   shell=True)


def main():
    if locked():
        if check_unlock_condition():
            unlock_session()
    else:
        if check_lock_condition():
            lock_session()
