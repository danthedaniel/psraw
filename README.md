PSRAW
===

[![PyPI version](https://badge.fury.io/py/psraw.svg)](https://badge.fury.io/py/psraw) [![Coverage Status](https://coveralls.io/repos/github/teaearlgraycold/psraw/badge.svg?branch=master)](https://coveralls.io/github/teaearlgraycold/psraw?branch=master) [![Build Status](https://travis-ci.org/teaearlgraycold/psraw.svg?branch=master)](https://travis-ci.org/teaearlgraycold/psraw) [![Code Health](https://landscape.io/github/teaearlgraycold/psraw/master/landscape.svg?style=flat)](https://landscape.io/github/teaearlgraycold/psraw/master)

pushshift reddit API wrapper

### Installation

psraw requires the installation of the `praw` package, so make sure
you have that installed first.

```bash
pip install psraw
```

*Both Python 2.7 and Python 3.X are supported*

### Usage

Each function in the library is a generator. This allows you to set an extremely
high limit parameter without the need to call the functions multiple times. To
get a normal Python list, just wrap the function with the `list()` constructor.

```python
import psraw
import praw

r = praw.Reddit(...)

# Get a list from the API
results = list(psraw.comment_search(r, q='teaearlgraycold', limit=30))

# Or use the function as a generator
for comment in psraw.comment_search(r, q='teaearlgraycold', limit=3000):
    # Do something with the comment
```

### Available functions

[Official Documentation](https://docs.google.com/document/d/171VdjT-QKJi6ul9xYJ4kmiHeC7t_3G31Ce8eozKp3VQ/edit)

In the example function signatures below, `r` is a `praw.Reddit` session object.
**All other arguments must be passed as keyword arguments.**

Each function will return either a list of `praw.models.Comment` objects or
`praw.models.Submission` objects.

```python
psraw.comment_search(r, q='', subreddit='', limit=0, sort='asc', after=0, before=0)
```

```python
psraw.comment_fetch(r, author='', subreddit='', limit=0, sort='asc', after=0, before=0)
```

```python
psraw.submission_search(r, q='', subreddit='', limit=0, sort='asc', after=0, before=0)
```

```python
psraw.submission_activity(r, limit=0, after=0, before=0)
```
