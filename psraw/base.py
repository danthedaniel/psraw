import requests
import praw

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


def sort_type(value):
    directions = ['asc', 'desc']

    if value in directions:
        return value
    else:
        raise ValueError('Value must be one of: {}'.format(directions))


base_address = 'https://apiv2.pushshift.io/reddit'
endpoints = {
    'comment_search': {
        'params': {
            'q': str,
            'subreddit': str,
            'limit': int,
            'sort': sort_type,
            'after': int,
            'before': int
        },
        'return_type': praw.models.Comment,
        'url': '/search/comment/'
    },
    'comment_fetch': {
        'params': {
            'author': str,
            'after': int,
            'before': int,
            'limit': int,
            'subreddit': str,
            'sort': sort_type
        },
        'return_type': praw.models.Comment,
        'url': '/comment/fetch/'
    },
    'submission_search': {
        'params': {
            'q': str,
            'subreddit': str,
            'limit': int,
            'sort': sort_type,
            'after': int
        },
        'return_type': praw.models.Submission,
        'url': '/search/submission/'
    },
    'submission_activity': {
        'params': {
            'limit': int,
            'before': int,
            'after': int
        },
        'return_type': praw.models.Submission,
        'url': '/submission/activity/'
    }
}


def create_endpoint_function(name, config):
    def endpoint_func(r, **kwargs):
        coerced_kwargs = {}

        for key, value in list(kwargs.items()):
            try:
                coerced_kwargs[key] = config['params'][key](value)
            except KeyError:
                raise ValueError(
                    '{} parameter is not accepted by {} endpoint'.
                    format(key, name)
                )

        query_params = '?{}'.format(urlencode(coerced_kwargs))
        resp = requests.get('{}{}{}'.format(base_address, config['url'], query_params))
        return [config['return_type'](r, _data=x) for x in resp.json()['data']]

    endpoint_func.__name__ = name
    return endpoint_func


for name, config in list(endpoints.items()):
    print('Creating func: {}'.format(name))
    globals()[name] = create_endpoint_function(name, config)

