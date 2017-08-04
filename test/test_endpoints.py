import praw
import psraw
import vcr
import os
import types
from psraw.endpoints import ENDPOINTS


LIMIT = 10
r = praw.Reddit(
    client_id='BfP08bO63oqXEA',
    client_secret='ofMkrQESZ2bC9Qi2S9V5bBhyZMA',
    user_agent='psraw v{} nosetests'.format(psraw.__version__)
)


def test_psraw_exports():
    """psraw exports a function for every endpoint specified in ENDPOINTS"""
    endpoint_names = set(ENDPOINTS.keys())
    psraw_exports = set(dir(psraw))
    assert endpoint_names.issubset(psraw_exports)


@vcr.use_cassette('test/cassettes/comment_search.yaml')
def test_comment_search():
    """comment_search returns a list of praw.models.Comment objects"""
    comments = list(psraw.comment_search(r, q='automoderator', limit=LIMIT))
    assert len(comments) == LIMIT
    assert isinstance(comments[0], praw.models.Comment)


@vcr.use_cassette('test/cassettes/comment_search_large.yaml')
def test_comment_search_2():
    """comment_search works with limit requiring multiple requests"""
    comment_search_limit = ENDPOINTS['comment_search']['limit']
    large_limit = comment_search_limit * 2
    comments = psraw.comment_search(r, q='automoderator', limit=large_limit)
    assert isinstance(comments, types.GeneratorType)
    assert len(list(comments)) == large_limit


@vcr.use_cassette('test/cassettes/submission_search.yaml')
def test_submission_search():
    """submission_search returns a list of praw.models.Submission objects"""
    submissions = list(psraw.submission_search(r, q='automoderator', limit=LIMIT))
    assert len(submissions) == LIMIT
    assert isinstance(submissions[0], praw.models.Submission)


@vcr.use_cassette('test/cassettes/submission_search_large.yaml')
def test_submission_search():
    """submission_search raises ValueError with large limits in desc sort"""
    submission_search_limit = ENDPOINTS['submission_search']['limit']
    large_limit = submission_search_limit * 2

    try:
        list(psraw.submission_search(r, q='automoderator', sort='desc', limit=large_limit))
        raise AssertionError
    except ValueError:
        pass  # Expected exception
