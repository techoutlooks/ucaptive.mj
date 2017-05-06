
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.views import exception_handler

__author__ = 'ceduth'


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {}
        errors = []
        for field, value in response.data.items():
            errors.append("{} : {}".format(field, " ".join(value)))

        response.data['errors'] = errors
        response.data['status'] = 'error'

        response.data['exception'] = getattr(exc, 'detail', 'Unkown Error')
    return response
