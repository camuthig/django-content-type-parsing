from typing import Type, List, Optional, TypeVar

from django.http import HttpRequest as _HttpRequest
from django.http import QueryDict
from django.utils.datastructures import MultiValueDict

from django_content_parsing import parsers
from django_content_parsing.parsers import BaseParser


BP = TypeVar("BP", bound=BaseParser)


class ContentParsingMixin:
    """
    A mixin that adds support for parsing request content.

    The behaviors of this mixin should be added directly to
    django.http.HttpRequest when merged into Django core. It is a mixin within
    this proof of concept to avoid init conflicts with ASGIRequest and WSGIRequest
    """
    def _load_post_and_files(
            self,
            data_attr="_post",
            parser_list: Optional[List[Type[BP]]] = None,
            methods=("POST",),
    ):
        """
        An override of Django's internal _load_post_and_files method.

        The behaviors here will be integrated into Django core when the DEP is accepted.
        """
        # WIP
        if methods and self.method not in methods:
            # Note: a method was provided but doesn't match the method set on
            # the request. In this case, we are not handling any real
            # behaviors and setting empty values. This matches how Django
            # previously handled all non-POST requests.
            self._post, self._files = (
                QueryDict(encoding=self._encoding),
                MultiValueDict(),
            )
            return
        if self._read_started and not hasattr(self, "_body"):
            # WIP Not sure why this is needed
            setattr(self, data_attr, QueryDict())
            self._files = MultiValueDict()

        if parser_list is None:
            parser_list = [parsers.FormParser, parsers.MultiPartParser]

        selected_parser: Type[BP] | None = None
        for p in parser_list:
            if p.can_handle(self.content_type):
                selected_parser = p
                break

        if selected_parser is not None:
            parser: BaseParser = selected_parser(self)
            try:
                if self.content_type == "multipart/form-data":
                    parser.parsers = (p(self) for p in parser_list)
                    data, self._files = parser.parse(None)
                else:
                    data, self._files = parser.parse(self.body)
                setattr(self, data_attr, data)
            except Exception as e:
                # TODO 'application/x-www-form-urlencoded' didn't do this.
                # An error occurred while parsing POST data. Since when
                # formatting the error the request handler might access
                # self.POST, set self._post and self._file to prevent
                # attempts to parse POST data again.
                setattr(self, data_attr, QueryDict())
                self._files = MultiValueDict()
                raise e
        else:
            data, self._files = (
                QueryDict(encoding=self._encoding),
                MultiValueDict(),
            )
            setattr(self, data_attr, data)

    @property
    def parsers(self):
        return self._parsers

    @parsers.setter
    def parsers(self, parsers):
        if hasattr(self, "_data") or hasattr(self, "_files"):
            raise AttributeError(
                "You cannot change parsers after processing the request's content."
            )
        self._parsers = parsers

    @property
    def data(self):
        if not hasattr(self, "_data"):
            self._load_post_and_files("_data", self.parsers, methods=None)
        return self._data

    @data.setter
    def data(self, data):
        self._data = data


class HttpRequest(ContentParsingMixin, _HttpRequest):
    """
    A subclass of Django's HttpRequest that supports content parsing.

    This is used only for better type hinting at this phase.
    """
    pass