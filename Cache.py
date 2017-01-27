"""
Implements a thread-safe key-value store
"""
import threading
import Config
import time

from errors import *
import logging

logger = logging.getLogger(__name__)


class RequestCache(object):
    def __init__(self, key, count):
        self.key = key
        self.count = count
        self.__lock = threading.Lock()

    def get_count(self, acquire_lock = True):
        if acquire_lock:
            self.__lock.acquire()
            ret = self.count
            self.lock.release()
        else:
            ret =  self.count
        return ret

    def decr_count(self):
        self.__lock.acquire()
        reached_zero = False
        if self.count < 1:
            reached_zero = True
        else:
            self.count -= self.count
        self.__lock.release()

        if reached_zero:
            raise TooManyRequestsException


class APILimitsCache(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_throttle_limits = Config.KEY_SPECIFIC_LIMITS.get(self.api_key, Config.get_global_defaults())
        self.__throttled_till = 0
        self.__lock = threading.Lock()
        self.__request_cache = {}

    def check_request_cache_exists(self, cache_key):
        return self.__request_cache.get(cache_key)

    def create_request_cache(self, cache_key):
        count = self.api_throttle_limits['count'] - 1
        self.__lock.acquire()
        print "CREATING REQUEST CACHE ", cache_key
        if not self.__request_cache.get(cache_key):
            self.__request_cache[cache_key] = RequestCache(cache_key, count)
        self.__lock.release()
        return self.__request_cache[cache_key]

    def generate_request_cache_key(self, start_time):
        bucket = start_time // self.api_throttle_limits['window']
        return self.api_key + '|' + str(bucket)

    def accessed(self):
        __start = time.time()
        if self.__throttled_till > __start:
            raise APISuspendedException

        # API is not throttled already
        request_cache_key = self.generate_request_cache_key(__start)
        if self.check_request_cache_exists(request_cache_key):
            print "Request cache exists "
            # This has been accessed before
            request_cache_obj = self.__request_cache[request_cache_key]
            curr_count = request_cache_obj.get_count(acquire_lock = False)
            print "current count ", curr_count
            if curr_count > 0:
                try:
                    request_cache_obj.decr_count()
                    print "decrementing counter ", request_cache_obj.get_count(acquire_lock = False)
                except TooManyRequestsException:
                    print "too many exceptions "
                    self.__lock.acquire()
                    self.__throttled_till = __start + self.api_throttle_limits['suspension']
                    self.__lock.release()
                    raise
            else:
                raise TooManyRequestsException
        else:
            self.create_request_cache(request_cache_key)

    def cull(self):
        # get rid of older windows
        pass
