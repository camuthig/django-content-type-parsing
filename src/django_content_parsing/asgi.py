from django.core.handlers.asgi import ASGIHandler as _ASGIHandler
from django.core.handlers.asgi import ASGIRequest as _ASGIRequest

from django_content_parsing import parsers
from django_content_parsing.request import HttpRequest


class ASGIRequest(HttpRequest, _ASGIRequest):
    def __init__(self, scope, body_file):
        super().__init__(scope, body_file)
        self._parsers = [
            parsers.FormParser,
            parsers.MultiPartParser,
            parsers.JSONParser,
        ]


class ASGIHandler(_ASGIHandler):
    request_class = ASGIRequest


def get_asgi_application():
    import django

    django.setup(set_prefix=False)
    return ASGIHandler()