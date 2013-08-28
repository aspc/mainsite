#/usr/bin/env python
# Uses vagrant to execute a reload command on the guest VM when
# source files are changed
#
# Depends on python-watchdog >= 0.6.0
import os, os.path
import time
import subprocess
import logging
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

RELOAD_CMD = "vagrant ssh -c \"sudo service gunicorn reload\""
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
SOURCE_ROOT = os.path.join(REPO_ROOT, 'aspc')
WATCH_FILE_PATTERNS = ("*.py", "*.html")

class ReloadGunicornHandler(PatternMatchingEventHandler):
    def on_any_event(self, event):
        logging.info("Reloading... ({0})".format(event))
        timer = time.time()
        try:
            subprocess.check_call(RELOAD_CMD, shell=True)
        except subprocess.CalledProcessError as ex:
            logging.exception("Couldn't reload via Vagrant!")
        finally:
            logging.info("Done in {0} sec".format(time.time() - timer))

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')
    event_handler = ReloadGunicornHandler(patterns=WATCH_FILE_PATTERNS)
    observer = Observer()
    observer.schedule(event_handler, path=SOURCE_ROOT, recursive=True)
    observer.start()
    logging.info("Watching for changes in {0} to {1}".format(SOURCE_ROOT, WATCH_FILE_PATTERNS))
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
