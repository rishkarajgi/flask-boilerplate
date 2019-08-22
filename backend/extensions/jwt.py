import os

import redis
from flask_jwt_extended import (JWTManager, create_access_token,
                                create_refresh_token, get_jwt_claims,
                                get_jwt_identity, jwt_optional,
                                jwt_refresh_token_required, jwt_required,
                                verify_jwt_in_request)
from flask_jwt_extended.exceptions import (CSRFError, FreshTokenRequired,
                                           InvalidHeaderError,
                                           NoAuthorizationError, UserLoadError)
from flask_jwt_extended.utils import (decode_token, has_user_loader,
                                      user_loader, verify_token_claims,
                                      verify_token_not_blacklisted,
                                      verify_token_type)
from jwt import ExpiredSignatureError
from werkzeug.exceptions import BadRequest

revoked_jwt_store = redis.StrictRedis(
    host=os.getenv('FLASK_REDIS_HOST', '127.0.0.1'),
    port=os.getenv('FLASK_REDIS_PORT', 6379),
    db=0, decode_responses=True
)

jwt_manager = JWTManager()


@jwt_manager.token_in_blacklist_loader
def check_if_token_is_revoked(decrypted_token):
    jti = decrypted_token['jti']
    entry = revoked_jwt_store.get(jti)
    if entry is None:
        return False
    return entry == 'true'


def decode_jwt_from_json(request, request_type, allow_missing_token=False):
    if request.content_type != 'application/json':
        raise NoAuthorizationError(
            'Invalid content-type. Must be application/json.')

    if request_type == 'access':
        token_key = 'access_token'
    else:
        token_key = 'refresh_token'

    try:
        encoded_token = request.get_json().get(token_key)
        if not encoded_token:
            if allow_missing_token:
                return None
            else:
                raise BadRequest()
    except BadRequest:
        raise NoAuthorizationError(
            'Missing "{}" key in json data.'.format(token_key))

    decoded_token = None
    decoded_token = decode_token(encoded_token, None)
    verify_token_type(decoded_token, expected_type=request_type)
    verify_token_not_blacklisted(decoded_token, request_type)
    return decoded_token


__all__ = [
    'JWTManager',
    'create_access_token',
    'create_refresh_token',
    'get_jwt_claims',
    'get_jwt_identity',
    'jwt_optional',
    'jwt_refresh_token_required',
    'jwt_required',
    'verify_jwt_in_request',
    'CSRFError',
    'FreshTokenRequired',
    'InvalidHeaderError',
    'NoAuthorizationError',
    'UserLoadError',
    'decode_token',
    'has_user_loader',
    'user_loader',
    'verify_token_claims',
    'verify_token_not_blacklisted',
    'verify_token_type',
    'ExpiredSignatureError',
]
