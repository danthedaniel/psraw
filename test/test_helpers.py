from nose.tools import assert_raises
import praw
from psraw.base import limit_chunk, coerce_kwarg_types
from psraw.endpoints import sort_type


test_config = {
    'params': {
        'foo': str,
        'bar': int
    },
    'return_type': praw.models.Comment,
    'url': '/foo/bar'
}


def test_limit_chunk_1():
    """limit_chunk returns an array as expected with two positive arguments"""
    chunks = limit_chunk(333, 100)
    assert chunks == [100, 100, 100, 33]


def test_limit_chunk_2():
    """limit_chunk raises a ValueError when given a limit_max < 1"""
    assert_raises(ValueError, limit_chunk, 100, 0)


def test_limit_chunk_3():
    """limit_chunk returns an empty list if limit is < 1"""
    chunks = limit_chunk(-1, 100)
    assert chunks == []


def test_coerce_kwarg_types_1():
    """coerce_kwarg_types raises a ValueError when passed an unspecd argument"""
    kwargs = {'foobar': 24}
    assert_raises(ValueError, coerce_kwarg_types, kwargs, test_config['params'])


def test_coerce_kwarg_types_2():
    """coerce_kwarg_types converts parameter types"""
    kwargs = {
        'foo': 24,
        'bar': 25
    }
    coerced_kwargs = coerce_kwarg_types(kwargs, test_config['params'])
    assert isinstance(coerced_kwargs['foo'], str)
    assert isinstance(coerced_kwargs['bar'], int)


def test_sort_type_1():
    """sort_type returns the value passed in if it is a valid direction"""
    assert sort_type('asc') == 'asc'


def test_sort_type_2():
    """sort_type raises a ValueError if the value passed in is not a direction"""
    assert_raises(ValueError, sort_type, 'foobar')
