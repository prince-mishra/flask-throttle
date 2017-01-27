import unittest
import requests

from config import SERVER_URL


class TestBasicSearchByCity(unittest.TestCase):
    def test_search_city_200(self):
        city = 'Amsterdam'
        expected = ["13", "2", "4", "26", "23", "9"]
        url = SERVER_URL + 'search_by_city?city=%s' % city
        r = requests.get(url, headers = {'Authorization' : 'UIOPA'})
        self.assertEqual(r.status_code, 200)
        hotel_ids = [h['hotel_id'] for h in r.json()['hotels']]

        # the ordering of elements in the list is handled automatically
        self.assertEquals(hotel_ids, expected)

    def test_search_city_200_desc(self):
        city = 'Amsterdam'
        expected = ["13", "2", "4", "26", "23", "9"]
        expected.reverse()
        url = SERVER_URL + 'search_by_city?city=%s&order=DESC' % city
        r = requests.get(url, headers = {'Authorization' : 'UIOPA'})
        self.assertEqual(r.status_code, 200)
        hotel_ids = [h['hotel_id'] for h in r.json()['hotels']]

        # the ordering of elements in the list is handled automatically
        self.assertEquals(hotel_ids, expected)