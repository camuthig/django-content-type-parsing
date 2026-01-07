from django.core.handlers.wsgi import WSGIHandler as _WSGIHandler
from django.core.handlers.wsgi import WSGIRequest as _WSGIRequest

from django_content_parsing import parsers
from django_content_parsing.request import ContentParsingMixin


class WSGIRequest(ContentParsingMixin, _WSGIRequest):
    def __init__(self, environ):
        super().__init__(environ)
        self._parsers = [
            parsers.FormParser,
            parsers.MultiPartParser,
            parsers.JSONParser,
        ]


class WSGIHandler(_WSGIHandler):
    request_class = WSGIRequest


def get_wsgi_application():
    """
    The public interface to Django's WSGI support. Return a WSGI callable.

    Avoids making django.core.handlers.WSGIHandler a public API, in case the
    internal WSGI implementation changes or moves in the future.
    """
    import django

    django.setup(set_prefix=False)
    return WSGIHandler()
