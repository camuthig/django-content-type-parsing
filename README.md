# Django Request Content-Type Parsing

This package is a proof-of-concept implementation of the [content-type parsing DEP](https://github.com/django/deps/pull/88).
The goal is to demonstrate how the changes in this DEP will be implemented and behave when merged into Django.

There are a few purposes to this package.

First, the package implements automatic content-type parsing for JSON requests in Django. It also creates mechanisms
to easily add additional content-type parsers on a per-view basis.

Second, it updates the naming of the primary request attributes in the Django request object.

* `FILES` -> `files`
* `POST` -> `form_data`
* `GET` -> `query_params`
* `COOKIES` -> `cookies`

The original fields are still available for backwards compatibility, and each of the new attributes behaves exactly
as the original.

Finally, it adds a new `data` attribute to replace `POST`/`form_data`. This new attribute uses the new content-type
parsing mechanism instead of relying on the old Django behaviors. Only `data` or `POST`/`form_data` can be used in a 
single request. Attempting to use both will raise an exception. 

Most of the implementation is converted from this [pull request](https://github.com/django/django/pull/17546).

# How to Use This Package

## Install the Package

Install the package with

WIP Finish the pip setup and be sure of the name

```bash
uv add django-content-type-parsing
```

## Replace the Django HttpRequest

This package requires replacing the `HttpRequest` class used by Django, which in turn requires replacing the ASGI and 
WSGI handlers. In your `asgi.py` file, you will need to import and use `django_content_parsing.asgi.get_asgi_application`,
and in your `wsgi.py` file, you will need to import and use `django_content_parsing.wsgi.get_wsgi_application`.

```python
# asgi.py

import os

from django_content_parsing.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'example.settings')

application = get_asgi_application()
```

```python
# wsgi.py

import os

from django_content_parsing.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'example.settings')

application = get_wsgi_application()
```

## Use the New `data` Attribute

In your views, you can now use `request.data` instead of `request.POST`. If the request is sent with 
`Content-Type: application/json`, then the JSON will automatically be parsed for you.

```python
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django_content_parsing.request import HttpRequest

@csrf_exempt
def write_json(request: HttpRequest):
    return JsonResponse({"message": f"JSON message: {request.data['message']}"})
```

## Customize Content-Type Parsing

By default, Django will parse `application/json`, `application/x-www-form-urlencoded`, and `multipart/form-data`
content-types. If you would like to add additional content-types, this will need to be implemented as a custom parser
and added to the view's request.

The request's `parsers` attribute should be set to include the new parsers. The parsers are called in order, and the
first matching the content-type will be used. Setting the request's parsers after accesing `FILES`/`files`, 
`POST`/`form_data`, or `data` will raise an exception.

By default, parsers will match based on the `media_type` on the class. If a move complex behavior is required, then the
`can_handle` method can be overridden.

```python
import json

from django.http import HttpRequest, HttpResponse
from django.utils.datastructures import MultiValueDict

from django_content_parsing.parsers import BaseParser

class CustomVndJsonParser(BaseParser):
    media_type = 'application/vnd.custom+json'

    def parse(self, data):
        return json.loads(data), MultiValueDict()


def custom_json_view(request: HttpRequest):
    # Override the request's parsers before calling 
    request.parsers = [CustomVndJsonParser]

    data = request.data

    # do your work
    return HttpResponse()
```

Alternatively, a middleware could be used to apply custom parsers to all requests.

# History of This Change

This change has been a work in progress for over a decade, starting with
[this ticket](https://code.djangoproject.com/ticket/21442) from 2013 where the idea of configured request parsing was
first introduced. 

It was nearly merged in [2021](https://code.djangoproject.com/ticket/32259), however, it was decided that the changes
would be too disruptive. This did lead to 
[good discussions](https://forum.djangoproject.com/t/request-for-steering-council-vote-on-modernising-the-request-object/26816) 
on what would make the attribute renaming worthwhile. Specifically, it was decided that getting new functionality, like
content-type parsing, would make it more worthwhile. Both points needed to go fully through the DEP process
and be considered by the steering council to proceed.
