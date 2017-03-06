import praw
import psraw
import vcr
import os
import types
from psraw.endpoints import LIMIT_MAX, ENDPOINTS


LIMIT = 10
r = praw.Reddit(
    client_id=os.environ['CLIENT_ID'],
    client_secret=os.environ['CLIENT_SECRET'],
    user_agent='psraw v{} nosetests'.format(psraw.__version__)
)


def test_psraw_exports():
    """psraw exports a function for every endpoint specified in ENDPOINTS"""
    endpoint_names = set(ENDPOINTS.keys())
    psraw_exports = set(dir(psraw))
    assert endpoint_names.issubset(psraw_exports)


@vcr.use_cassette('test/cassettes/comment_fetch.yaml')
def test_comment_fetch():
    """comment_fetch returns a list of praw.models.Comment objects"""
    comments = list(psraw.comment_fetch(r, author='automoderator', limit=LIMIT))
    assert len(comments) == LIMIT
    assert isinstance(comments[0], praw.models.Comment)


@vcr.use_cassette('test/cassettes/comment_search.yaml')
def test_comment_search():
    """comment_search returns a list of praw.models.Comment objects"""
    comments = list(psraw.comment_search(r, q='automoderator', limit=LIMIT))
    assert len(comments) == LIMIT
    assert isinstance(comments[0], praw.models.Comment)


@vcr.use_cassette('test/cassettes/comment_search_large.yaml')
def test_comment_search_2():
    """comment_search returns a list of praw.models.Comment objects"""
    large_limit = LIMIT_MAX * 2
    comments = psraw.comment_search(r, q='automoderator', limit=large_limit)
    assert isinstance(comments, types.GeneratorType)
    assert len(list(comments)) == large_limit


# submission_activity test is disabled because it's only returning 500 errors
# @vcr.use_cassette('cassettes/submission_activity.yaml')
# def test_submission_activity():
#     """submission_activity returns a list of praw.models.Submission objects"""
#     submissions = list(psraw.submission_activity(r, limit=LIMIT))
#     assert len(submissions) == LIMIT
#     assert isinstance(submissions[0], praw.models.Submission)


@vcr.use_cassette('test/cassettes/submission_search.yaml')
def test_submission_search():
    """submission_search returns a list of praw.models.Submission objects"""
    submissions = list(psraw.submission_search(r, q='automoderator', limit=LIMIT))
    assert len(submissions) == LIMIT
    assert isinstance(submissions[0], praw.models.Submission)
