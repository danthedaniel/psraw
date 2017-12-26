import praw


def sort_type(value):
    """Ensures values passed in are one of the valid set"""
    directions = {'asc', 'desc'}

    if value in directions:
        return value
    else:
        raise ValueError('Value must be one of: {}'.format(directions))


LIMIT_DEFAULT = 50
BASE_ADDRESS = 'https://apiv2.pushshift.io/reddit'
ENDPOINTS = {
    'comment_search': {
        'params': {
            'after': int,
            'before': int,
            'limit': int,
            'q': str,
            'sort': sort_type,
            'subreddit': str,
            'author': str
        },
        'limit': 500,
        'return_type': praw.models.Comment,
        'url': '/search/comment/'
    },
    'submission_search': {
        'params': {
            'after': int,
            'limit': int,
            'q': str,
            'sort': sort_type,
            'subreddit': str
        },
        'limit': 250,
        'return_type': praw.models.Submission,
        'url': '/search/submission/'
    }
}
