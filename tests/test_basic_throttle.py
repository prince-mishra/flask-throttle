import unittest
import grequests
import time

from config import SERVER_URL


class TestBasicThrottle(unittest.TestCase):
    # def test_no_throttling(self):
    #     city = 'Amsterdam'
    #     url = SERVER_URL + 'search_by_city?city=%s' % city
    #
    #     # make 5 parallel requests
    #     rs = (grequests.get(url, headers = {'Authorization' : 'THROTTLE_10_IN_2'}) for i in range(10))
    #     responses = grequests.map(rs)
    #
    #     # Since API key allows 10 requests every 2 seconds, these should all be successful
    #     for r in responses:
    #         self.assertEqual(r.status_code, 200)

    # def test_throttle_once(self):
    #     city = 'Amsterdam'
    #     url = SERVER_URL + 'search_by_city?city=%s' % city
    #
    #     # make 5 parallel requests
    #     rs = (grequests.get(url, headers={'Authorization': 'THROTTLE_10_IN_2_b'}) for i in range(10))
    #     responses = grequests.map(rs)
    #
    #     # Since API key allows 10 requests every 2 seconds, these should all be successful
    #     for r in responses:
    #         self.assertEqual(r.status_code, 200)
    #
    #     # allowed limits have been consumed
    #     # these requests should fail
    #     rs = (grequests.get(url, headers={'Authorization': 'THROTTLE_10_IN_2_b'}) for i in range(2))
    #     responses = grequests.map(rs)
    #     for r in responses:
    #         self.assertEqual(r.status_code, 429)

    def test_throttle_and_check_after_suspension_period(self):
        city = 'Amsterdam'
        url = SERVER_URL + 'search_by_city?city=%s' % city

        # make 5 parallel requests
        rs = (grequests.get(url, headers={'Authorization': 'THROTTLE_10_IN_2_c'}) for i in range(10))
        responses = grequests.map(rs)

        # Since API key allows 10 requests every 2 seconds, these should all be successful
        for r in responses:
            self.assertEqual(r.status_code, 200)

        # allowed limits have been consumed
        # these requests should fail
        rs = (grequests.get(url, headers={'Authorization': 'THROTTLE_10_IN_2_c'}) for i in range(2))
        responses = grequests.map(rs)
        for r in responses:
            self.assertEqual(r.status_code, 429)

        # API key is suspended for 5 seconds
        # Let's check after 5 seconds
        time.sleep(5)

        # make 5 parallel requests
        rs = (grequests.get(url, headers={'Authorization': 'THROTTLE_10_IN_2_c'}) for i in range(10))
        responses = grequests.map(rs)

        # Since API key allows 10 requests every 2 seconds, these should all be successful
        for r in responses:
            self.assertEqual(r.status_code, 200)

        # allowed limits have been consumed
        # these requests should fail
        rs = (grequests.get(url, headers={'Authorization': 'THROTTLE_10_IN_2_c'}) for i in range(2))
        responses = grequests.map(rs)
        for r in responses:
            self.assertEqual(r.status_code, 429)