import requests
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode
from .endpoints import ENDPOINTS, BASE_ADDRESS, LIMIT_DEFAULT


def limit_chunk(limit, limit_max):
    """Return a list of limits given a maximum that can be requested per API
    request

    :param limit: The total number of items requested
    :param limit_max: The maximum number of items that can be requested at once
    """
    if limit_max < 1:
        raise ValueError('limit_max must be > 0')

    limits = []
    x = 0

    while x < limit:
        limits.append(min(limit_max, limit - x))
        x += limit_max

    return limits


def coerce_kwarg_types(kwargs, param_types):
    """Return a dict with its values converted to types specified in param_types

    :param kwargs: The dict of parameters passed to the endpoint function
    :param param_types: The dict of all valid parameters and their types (taken
        from the 'param' key of the endpoint config)
    """
    params = list(kwargs.items())
    try:
        return {key: param_types[key](value) for key, value in params}
    except KeyError as e:
        raise ValueError('{} parameter is not accepted'.format(e.args[0]))


def create_endpoint_function(name, config):
    """Dynamically create a function that handles a single API endpoint

    :param name: The name of the endpoint, which will also become the name of
        the function
    :param config: The configuration of the API endpoint
    """
    def endpoint_func(r, **kwargs):
        """Placeholder that becomes an endpoint handler through closure

        :param r: A reddit session object that is passed to instantiated
            Comment or Submission objects
        :param **kwargs: Query parameters passed to the API endpoint
        """
        coerced_kwargs = coerce_kwarg_types(kwargs, config['params'])
        direction = 'before'

        if 'limit' not in coerced_kwargs:
            coerced_kwargs['limit'] = LIMIT_DEFAULT
        if coerced_kwargs.get('sort', None) == 'asc':
            direction = 'after'

        # Loop over the API request, since multiple may be required if the
        # specified limit is greater than config['limit']
        for limit in limit_chunk(coerced_kwargs['limit'], config['limit']):
            coerced_kwargs['limit'] = limit
            query_params = urlencode(coerced_kwargs)
            url = '{}{}?{}'.format(BASE_ADDRESS, config['url'], query_params)
            data = requests.get(url).json()['data']

            for item in data:
                yield config['return_type'](r, _data=item)

            if len(data) < limit:
                raise StopIteration

            if direction in config['params']:
                # On subsequent requests, specify that we only want results from
                # before or after the last item we were sent
                coerced_kwargs[direction] = data[-1]['created_utc']
            elif int(kwargs['limit']) > config['limit']:
                raise ValueError(
                    'Can not perform requests of > {} because this endpoint can'
                    'not specify the {} query parameter.'.
                    format(config['limit'], direction)
                )

    endpoint_func.__name__ = name
    return endpoint_func


for name, config in list(ENDPOINTS.items()):
    globals()[name] = create_endpoint_function(name, config)
