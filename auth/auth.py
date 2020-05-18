import json
from flask import request, _request_ctx_stack, abort
# , session, redirect
from functools import wraps
from jose import jwt
from urllib.request import urlopen
import http.client


AUTH0_DOMAIN = 'udacity-nd-capstone.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'casting'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

    def to_dict(self):
        return {"message": self.error, "status_code": self.status_code}

## Auth Header

'''
@TODO implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''


def get_token_auth_header():
    # get_token_header()
    print('get_token_auth_header request.headers')
    auth = request.headers.get('Authorization', None)
    if not auth:
       raise AuthError({
           'code': 'authorization_header_missing',
           'description': 'Authorization header is expected.'
       }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
       print('in1', parts[0].lower())
       raise AuthError({
           'code': 'invalid_header',
           'description': 'Authorization header must start with "Bearer".'
       }, 401)

    elif len(parts) == 1:
       print('in12')
       raise AuthError({
           'code': 'invalid_header',
           'description': 'Token not found.'
       }, 401)

    elif len(parts) > 2:
       print('in3')
       raise AuthError({
           'code': 'invalid_header',
           'description': 'Authorization header must be bearer token.'
       }, 401)

    # print('in 5')
    token = parts[1]
    # print('Before return in get_token_auth_header')
    return token

'''
@TODO implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
'''

def check_permissions(permission, payload):
    print('In Check Permission')
    if payload is None:
        raise AuthError({
            'code': 'No_payload',
            'description': 'payload is None.'
        }, 400)

    if 'permissions' not in payload:
        # abort(400)
        raise AuthError({
            'code': 'permissions_payload',
            'description': 'Permission not present in the payload.'
        }, 400)

    if permission not in payload['permissions']:
        # abort(403)
        raise AuthError({
            'code': 'permissions_payload',
            'description': 'Payload does not contain "permissions" string.'
        }, 403)

    return True

'''
@TODO implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload
    !!NOTE urlopen has a common certificate error described here:
    https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify
    -failed-error-for-http-en-wikipedia-org
'''


def verify_decode_jwt(token):
    # print('In verify', token)
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    # print('After jsonurl')
    jwks = json.loads(jsonurl.read())
    # print('Before unverified header', jwks)
    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}
    # print('before if kid', unverified_header['kid'])
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    # print('Before rsa_key', rsa_key)
    if rsa_key:
        try:
            # print('Inside Try')
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)

'''
@TODO implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the
    requested permission
    return the decorator which passes the decoded payload to the decorated
    method
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            # print('requires_auth', token)
            try:
                payload = verify_decode_jwt(token)
            except AuthError as err:
                abort(401, err.error)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator



def get_token_header():
    print('request.cookies', request.cookies)
    conn = http.client.HTTPSConnection("http://127.0.0.1:5000")

    headers = {
        'content-type': "application/json",
        'authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikg2U001cFZaSlRma25Ua0NQWFlzUyJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktbmQtY2Fwc3RvbmUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYjI2NDZkMWNjMWFjMGMxNDhhOTliOSIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1ODk3ODMxODAsImV4cCI6MTU4OTc5MDM4MCwiYXpwIjoiOUVhbGhIVFZVbXF3TW5uRjk0RFQwMEp1b0lIa1l0Y3giLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpsaXN0cyJdfQ.holaJz2IcvJTMGLEvqFrSDZ1966Uy-q1nWURo12OtnHzuZQes2nfHfdtciZkkpJ87qzsRs8QnB0lyrTAV90MZPtdbC0z_785vrvQQZN0kz6uh6kTulqpgwJUJwvRjrYN-q5wVMsD66FgkE6mj-Nl8RjlSdtBz7Bfjg89MzZ7c3fX2QG3En_uWpA2KOkJu71vYegvXd6QMDj9OaFb3AgF1-uv8Mocpa98lYMOEk-H_mB7KEy67eCG3ys59D4_c4-F43DMW680m7rvuLrAbbTzhqBOAD-EMOYsOdCXzTd7bPZvRSsJwrSicaOwiPBSiwz0JnQMV0YoD5EsD77nPCu2XQ"
        }

    conn.request("GET", "/", headers=headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))
