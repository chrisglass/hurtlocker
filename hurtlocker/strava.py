import datetime
import json
import os
import sys
import time

from http.server import HTTPServer, BaseHTTPRequestHandler

from stravalib import Client


# This should be configuration.
CLIENT_ID="CHANGEME"
CLIENT_SECRET="CHANGEME"


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


def get_tokens_from_disk():
    """Get the saved token from disk, or return an empty dict if there is none."""
    contents = {}
    if os.path.isfile(".hurtlocker"):
        with open(".hurtlocker", "r") as thefile:
            contents = thefile.read()

    if contents == {}:
        return contents

    return json.loads(contents)


def get_strava_token():
    """Return a valid strava token.

    This will initiate the OAUTH dance if needed (register or refresh), or just
    get the token from disk."""

    if get_tokens_from_disk() == {}:
        client = Client()
        url = client.authorization_url(client_id=CLIENT_ID,
                                       redirect_uri='http://127.0.0.1:5000/authorization')

        print("Please open this in your browser:" + url)

        server_address = ('', 5000)
        httpd = PainfulHTTPServer(server_address, StravaOauthRequestHandler)
        httpd.serve_until_stopped()

    # Now the file really shouldn't be empty anymore.
    tokens = get_tokens_from_disk()

    # Is our token expired?
    now = datetime.datetime.now()
    if now.timestamp() >= (tokens["expires_at"] - 10000): # 10 seconds leeway
        client = Client()
        refresh_response = client.refresh_access_token(
            client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
            refresh_token=tokens["refresh_token"])

        with open(".hurtlocker", "w") as thefile:
            thefile.write(json.dumps(refresh_response))

        tokens = get_tokens_from_disk()

    return tokens["access_token"]


def should_unlock(lock_time_of_day):
    """Determine whether the person registered an activity since lock time."""
    token = get_strava_token()
    client = Client(access_token=token)
    today = datetime.date.today()
    afterdate = datetime.datetime.combine(today, lock_time_of_day)

    activities = client.get_activities(after=afterdate.isoformat())
    activity_list = [a for a in activities]

    # Did the locked person record at least one activity since the lock time?
    if len(activity_list) > 0:
        return True
    return False
