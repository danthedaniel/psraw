import praw
import psraw
from psraw.endpoints import ENDPOINTS, sort_type


def test_psraw_exports():
    """psraw exports a function for every endpoint specified in ENDPOINTS"""
    endpoint_names = set(ENDPOINTS.keys())
    psraw_exports = set(dir(psraw))
    assert endpoint_names.issubset(psraw_exports)
