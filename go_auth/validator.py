""" An oauthlib.oauth2 request valditator for Vumi Go.
"""

from oauthlib.oauth2 import RequestValidator, WebApplicationServer


class AuthValidator(RequestValidator):
    """ An oauthlib.oauth2 request validator.
    """

    def __init__(self, backend):
        self._backend = backend

    def validate_bearer_token(self, token, scopes, request):
        stored_token = self._backend.get_token(request.client_id)
        if stored_token is None:
            return False
        if stored_token['access_token'] != token['access_token']:
            return False
        stored_scopes = stored_token['scopes'].split()
        available_scopes = set(stored_scopes) & set(scopes)
        # validate as true if any scopes are available
        return bool(available_scopes)

    def save_bearer_token(self, token, request, *args, **kw):
        self._backend.save_token(request.client_id, token)


def web_app_authenticator(backend):
    """ Return a Vumi Go web app authenticator.
    """
    validator = AuthValidator(backend)
    authenticator = WebApplicationServer(validator)
    return authenticator
