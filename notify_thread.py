import threading
import requests
import time
from notify import notify

class NotifyThread(threading.Thread):
    """Notify User of Bus Times
    """

    def __init__(self, route, stop, expire_time=30):
        threading.Thread.__init__(self)
        self.route = route
        self.stop = stop
        self.expire_time = expire_time*60 + time.time()

        # Set running to False to quit thread
        self.running = False

    def run(self):
        self.running = True

        initial_notify = False # Notify first that we are tracking
        five_or_below = False # Second notification at 5 minutes out
        one_or_below = False # Third notification at 1 minute out

        while self.running and time.time() < self.expire_time:
            print "Checking ETAs"

            # Attempt to get etas, if error sleep for 10 seconds
            # ENHANCEMENT: After so many errors kill the thread
            try:
                etas = self._get_etas()
                print "ETA: %s" % etas[0]
            except Exception:
                start = time.time()
                print "Error getting stop times."
                while time.time() < (start + 10) and self.running:
                    time.sleep(1)
                continue

            # When it's one minute out, notify us!
            if etas[0] <= 1:
                one_or_below = True
                notify("%d minute left, bus is coming!" % etas[0],
                       "http://mattmolo.com/1b/")

                # Stop running the thread
                self.running = False

            # When it's five minutes out, notify us!
            elif not five_or_below and etas[0] <= 5:
                five_or_below = True
                notify("%d minutes left, leave now!" % etas[0],
                       "http://mattmolo.com/1b/")
                self.expire_time = time.time() + 10*60

            # Otherwise, notify that we are tracking
            elif not initial_notify:
                notify("Tracking Bus: %d minutes left" % etas[0],
                       "http://mattmolo.com/1b/")

            initial_notify = True

            # Sleep for X seconds before checking again
            # When > 5, check every 10. When <= 5 check every 10
            start = time.time()
            if five_or_below:
                print "Sleeping for 10"

                while time.time() < (start + 10) and self.running:
                    time.sleep(1)
            else:
                print "Sleeping for 30"

                while time.time() < (start + 30) and self.running:
                    time.sleep(1)

        print "Finished"


    def _get_etas(self):
        """Grab etas from local server
        """
        etas = requests.get('http://localhost:4000/eta/%s/%s' %
                            (self.route, self.stop)).json()

        return etas['results']
