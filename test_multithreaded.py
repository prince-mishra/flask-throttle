from __future__ import absolute_import
import threading
import time

from Cache import APILimitsCache
from Config import KEY_SPECIFIC_LIMITS

authkeys = ['THROTTLE_10_IN_2_c', 'THROTTLE_10_IN_2_b']

API_CACHE_STORE = {}
for k in authkeys:
    API_CACHE_STORE[k] = APILimitsCache(k)


class RequestThread(threading.Thread):

    def __init__(self, name, api_key):
        threading.Thread.__init__(self)
        self.api_key = api_key
        self.name = name

    def run(self):
        print "Starting " + self.name
        access(self.name, self.api_key)
        print "Exiting " + self.name

def access(name, api_key):
    while True:
        try:
            API_CACHE_STORE[api_key].accessed()
        except Exception, fault:
            print str(fault)

        time.sleep(2)
        print "%s: %s %s" % (name, time.ctime(time.time()), API_CACHE_STORE[api_key])

# Create new threads
thread1 = RequestThread("Thread-1", "THROTTLE_10_IN_2_c")
thread2 = RequestThread("Thread-2", "THROTTLE_10_IN_2_c")

# Start new Threads
thread1.start()
thread2.start()

print "Exiting Main Thread"
