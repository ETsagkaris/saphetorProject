ACCEPT_HEADER_NOT_ACCEPTABLE = "accept_header_not_acceptable"
API_CALL_NOT_MODIFIED = "api_call_not_modified"
PERMISSION_DENIED = "permission_denied"
NO_VARIANTS_FOUND = "no_variants_found"


def camel_case(s):
    return s[0].lower() + s[1:]


class JsonException(Exception):
    def __init__(self, message='', data={}, details='', name='', code=500):
        self.message = message
        self.details = details
        self.data = data
        if not hasattr(self, 'code'):
            self.code = code
        self.name = name or camel_case(self.__class__.__name__)
        Exception.__init__(self, message, details, self.name, self.code)
