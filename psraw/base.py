import requests
import praw

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


def sort_type(value):
    directions = ['asc', 'desc']

    if value in self.directions:
        return value
    else:
        raise ValueError('Value must be one of: {}'.format(this.directions))


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
    }
}


for name, config in list(endpoints.items()):
    def req_endpoint(r, **kwargs):
        coerced_kwargs = {}

        for key, value in list(kwargs.items()):
            try:
                coerced_kwargs[key] = config['params'][key](value)
            except KeyError:
                raise ValueError(
                    '{} parameter is not accepted by {} endpoint'.
                    format(key, name)
                )

        if len(coerced_kwargs) > 0:
            query_params = urlencode(coerced_kwargs)
        else:
            query_params = ''

        resp = requests.get('{}{}{}'.format(base_address, config['url'], query_params))
        return [config['return_type'](r, _data=x) for x in resp.json()['data']]

    req_endpoint.__name__ = name
    globals()[name] = req_endpoint
