#/usr/bin/env python
import os
import sys
import time
import subprocess
import atexit
from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import PatternMatchingEventHandler

RELOAD_CMD = "/vagrant/vagrant/gunicorn.sh reload"
SOURCE_ROOT = "/vagrant/aspc/"
WATCH_FILE_PATTERNS = ("*.py", "*.html")

class ReloadGunicornHandler(PatternMatchingEventHandler):
    def on_any_event(self, event):
        print "Reloading", event
        # subprocess.check_call(RELOAD_CMD, shell=True)

if __name__ == "__main__":
    event_handler = ReloadGunicornHandler(patterns=WATCH_FILE_PATTERNS)
    observer = Observer()
    observer.schedule(event_handler, path=SOURCE_ROOT, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
