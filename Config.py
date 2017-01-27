API_DEFAULT_THROTTLE_WINDOW = 1 # second
API_DEFAULT_THROTTLE_COUNT = 150 # requests
API_DEFAULT_SUSPENDED_FOR = 5*60 # 5 minutes


def get_global_defaults():
    return {
        'window': API_DEFAULT_THROTTLE_WINDOW,
        'count': API_DEFAULT_THROTTLE_COUNT,
        'suspension': API_DEFAULT_SUSPENDED_FOR
    }

KEY_SPECIFIC_LIMITS = {
    'QWERTY': {
        'window': 1 * 60,
        'count': 5,
        'suspension': API_DEFAULT_SUSPENDED_FOR
    },
    'UIOPA': {
            'window': 5 * 60,
            'count': 50,
            'suspension': API_DEFAULT_SUSPENDED_FOR
    },
    'THROTTLE_10_IN_2': {
            'window': 2,
            'count': 10,
            'suspension': API_DEFAULT_SUSPENDED_FOR
    },
    'THROTTLE_10_IN_2_b': {
        'window': 2,
        'count': 10,
        'suspension': API_DEFAULT_SUSPENDED_FOR
    },
    'THROTTLE_10_IN_2_c': {
            'window': 2,
            'count': 10,
            'suspension': 5
        }

}

API_CACHE = {}