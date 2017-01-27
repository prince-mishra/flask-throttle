Problem 1: search_by_city API
=============================
As part of data loading, 2 objects are created:
1. A hotel_id to hotel_object map
2. a city to hotel_ids_in_that_city map. The list is sorted on increasing order of price

When a call to this API is made,
1. Get the list of hotel_ids for this city from second map which stores city wise hotel ids.
If order specified is 'DESC', this list is reversed
2. For each hotel_id in this list, get full object from first map and build the response

Optimisations:
1. I could store the entire hotel objects in the second map instead of hotel_ids only
and that would save one iteration over selected hotel ids to get the complete object.
However, the idea is to think of second map as some sort of an index which can be quickly O(1) queries to get a list of
ids and for these ids, full objects can be retrieved in O(1) from the store.

Problem 2: rate limiting
========================

1. API keys have specified rate limits in Config

2. The API keys in the Config are picked and a map of the form {'api_key' : API_LIMITS_CACHE } is created

3. API_LIMITS_CACHE is an object (a) which stores - is the API currently suspended? and (b) maintains a map RequestCache
for every limit interval

4. keys for RequestCache are generated using api_key + the bucket current request will fall in. Assume we are limiting
on a 1 minute window, then all requests for the current minute should map to the current minute bucket.

5. RequestCache.count is initialised with the number of requests it should support in the specified duration

6. Whenever a new request comes, the count is decremented and when the count becomes 0, a TooManyRequests exception is
raised. As a result, the parent object "APILimitsCache" is updated with the duration for which it should be marked
throttled.



```python
flask-throttle.py data/hoteldb.csv
```
