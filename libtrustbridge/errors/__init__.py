from http import HTTPStatus as StatusCode
from werkzeug import exceptions as werke
from .base import BaseError


# Error suffix is important because title and code are autogenerated
class ValidationError(BaseError):
    status = StatusCode.BAD_REQUEST


class MissingAttributesError(ValidationError):
    @staticmethod
    def create_detail(missing):
        return 'Missing required attributes: {}.'.format(missing)

    @staticmethod
    def create_source(missing):
        return missing

    def __init__(self, missing=None, **kwargs):
        if missing is not None:
            kwargs['detail'] = self.create_detail(missing)
            kwargs['source'] = self.create_source(missing)
        super().__init__(**kwargs)


# converts exceptions to proper json format
class InternalServerError(BaseError):
    status = StatusCode.INTERNAL_SERVER_ERROR

    @staticmethod
    def create_source(exception):
        return [
            {
                'type': exception.__class__.__name__,
                'str': str(exception)
            }
        ]

    def __init__(self, exception=None, **kwargs):
        if exception is not None:
            kwargs['detail'] = 'Unexpected server error occured.'
            kwargs['source'] = self.create_source(exception)
        super().__init__(**kwargs)


# converts werkzeug.HTTPException to proper json format
# this will create error with generic-http-error code
# this will indicate that error is default of
# some plugin or maybe just unhandled http exception

def fullclassname(cls):
    return '.'.join([cls.__module__, cls.__name__])


class GenericHTTPError(BaseError):
    status = StatusCode.BAD_REQUEST
    code = 'generic-http-error'

    def __init__(self, exception=None, **kwargs):
        if exception is not None:
            if not isinstance(exception, werke.HTTPException):
                try:
                    if isinstance(exception, int):
                        exception = werke.default_exceptions[exception]()
                    elif isinstance(exception, StatusCode):
                        exception = werke.default_exceptions[exception]()
                    else:
                        raise TypeError(
                            '{} "exception" kwarg must be the instance of: {}'.format(
                                self.__class__.__name__,
                                [
                                    fullclassname(werke.HTTPException),
                                    fullclassname(StatusCode),
                                    'int'
                                ]
                            )
                        )
                except KeyError as e:
                    raise ValueError(
                        'Non generic HTTP exception. Can\'t find class for status: "{}"'.format(str(e))
                    )
            kwargs['title'] = self.camel_case_to_title(exception.__class__.__name__)
            kwargs['status'] = exception.code
        super().__init__(**kwargs)


# Allows throwing several errors at once
# Has single attribute which can be set by
# args or directly after object initialization
# Because it's just a wrapper to support all standard requirements
# and functionality
class ErrorsList(Exception):
    """
        Throw several errors at once.
        Accepts only children of intergov.apis.common.base.BaseError
    """

    def __init__(self, *args):
        self.errors = args

    @property
    def errors(self):
        return self._errors

    @errors.setter
    def errors(self, value):
        for e in value:
            if not isinstance(e, BaseError):
                raise ValueError('All errors should be the instance of BaseError')
        self._errors = value


class UseCaseError(BaseError):

    # by default
    # code = 'use-case-error'

    @property
    def exception(self):
        exception, *rest = self.args
        return exception

    @property
    def detail(self):
        return self.exception.detail

    @property
    def source(self):
        return self.exception.source

    @property
    def title(self):
        return self.camel_case_to_title(self.exception.__class__.__name__)

    @property
    def status(self):
        return self.http_error_code_to_str(self.exception.status)

    @property
    def status_code(self):
        return self.exception.status

    @status_code.setter
    def status_code(self, value):
        # ignoring
        pass