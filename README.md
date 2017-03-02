PSRAW
===

[![PyPI version](https://badge.fury.io/py/psraw.svg)](https://badge.fury.io/py/psraw)

pushshift reddit API wrapper

### Installation

psraw requires the installation of the `praw` package, so make sure
you have that installed first.

```bash
pip install psraw
```

*Both Python 2.7 and Python 3.X are supported*

### Usage

```python
import psraw
import praw

r = praw.Reddit(...)

results = psraw.comment_search(r, q='teaearlgraycold', limit=30)
```

### Available functions

[Official Documentation](https://docs.google.com/document/d/171VdjT-QKJi6ul9xYJ4kmiHeC7t_3G31Ce8eozKp3VQ/edit)

In the example function signatures before, `r` is a `praw.Reddit` session object. 
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
psraw.submission_search(r, q='', subreddit='', limit=0, sort='asc', after=0)
```

```python
psraw.submission_activity(r, limit=0, after=0, before=0)
```
