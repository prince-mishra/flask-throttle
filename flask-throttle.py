import os
import csv
import logging

from flask import Flask
from flask import request, jsonify
from Cache import APILimitsCache
from logging import StreamHandler

from Config import API_CACHE, KEY_SPECIFIC_LIMITS

logger = logging.getLogger(__name__)


import Config
import time

from functools import wraps
from flask import request, Response

from errors import TooManyRequestsException, APISuspendedException
from Config import API_CACHE

def rate_limited_response():
    return Response('Too many requests', 429)


def unauthorized_response():
    return Response('Unauthorized', 401)


hotels = {}
city_wise_hotel_ids = {}

api_cache = {}


def is_rate_limited(api_key):
    api_cache = API_CACHE[api_key]
    try:
        api_cache.accessed()
    except TooManyRequestsException:
        print "Request limit reached "
        return True
    except APISuspendedException:
        print "API suspended"
        return True
    return False


def rate_limit(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('Authorization')
        if not api_key or not API_CACHE.get(api_key):
            return unauthorized_response()
        if is_rate_limited(api_key):
            return rate_limited_response()
        return func(*args, **kwargs)
    return decorated


def compare(id1, id2):
    return hotels[id1]['price'] - hotels[id2]['price']


def load_hotel_csv(filepath):
    if os.path.exists(filepath):

        with open(filepath, 'rU') as csvfile:
            csvreader = csv.reader(csvfile, dialect=csv.excel_tab)
            csvreader.next()
            for row in csvreader:
                print row
                city, hotel_id, room_type, price = row[0].split(',')
                hotel_obj = {
                    'city': city,
                    'hotel_id': hotel_id,
                    'room_type': room_type,
                    'price': int(price)
                }
                if city_wise_hotel_ids.get(city):
                    city_wise_hotel_ids[city].append(hotel_id)
                else:
                    city_wise_hotel_ids[city] = [hotel_id]

                hotels[hotel_id] = hotel_obj

        for city,hotels_ids in city_wise_hotel_ids.items():
            city_wise_hotel_ids[city] = sorted(hotels_ids, compare)


def build_api_cache():
    logger.info("BUILDING API CACHE")
    for k, v in KEY_SPECIFIC_LIMITS.items():
        API_CACHE[k] = APILimitsCache(k)

app = Flask(__name__)

@app.route('/search_by_city/<city>')
@rate_limit
def search_by_city(city):
    #print hotels
    hotel_ids = city_wise_hotel_ids[city]
    resp = {
        'hotels' : []
    }
    for hid in hotel_ids:
        resp['hotels'].append(hotels[hid])
    return jsonify(resp)

if __name__ == '__main__':
    import sys
    load_hotel_csv(sys.argv[1])
    build_api_cache()
    handler = StreamHandler()
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run()
