from _pytest import unittest
from itsdangerous import JSONWebSignatureSerializer, BadSignature, SignatureExpired
import calendar
import datetime

from sqlalchemy.sql.operators import is_
from sqlalchemy.testing import mock


def now():
    return calendar.timegm(datetime.datetime.utcnow().utctimetuple())


class TimedJSONWebSignatureSerializer(JSONWebSignatureSerializer):
    EXPIRES_IN_AN_HOUR = 3600

    def __init__(self, secret_key, salt=None, serializer=None, signer=None, signer_kwargs=None, algorithm_name=None,
                 expires_in=None):
        super(TimedJSONWebSignatureSerializer, self).__init__(secret_key, salt, serializer, signer, signer_kwargs,
                                                              algorithm_name)
        if not expires_in:
            expires_in = self.EXPIRES_IN_AN_HOUR
        self.expires_in = expires_in

    def loads(self, s, salt=None, return_header=False):
        payload = super(TimedJSONWebSignatureSerializer, self).loads(s, salt, return_header)

        if not 'exp' in payload:
            raise BadSignature("Missing ['exp'] expiry date", payload=payload)

        if not isinstance(payload['exp'], int) and payload['exp'] > 0:
            raise BadSignature("['exp'] expiry date is not and IntDate", payload=payload)

        if payload['exp'] < now():
            raise SignatureExpired(
                'Signature expired',
                payload=payload)

        return super(TimedJSONWebSignatureSerializer, self).loads(s, salt, return_header)

    def dumps(self, obj, salt=None, header_fields=None):
        iat = now()
        exp = iat + self.expires_in
        obj['iat'] = iat
        obj['exp'] = exp
        return super(TimedJSONWebSignatureSerializer, self).dumps(obj, salt=salt, header_fields=header_fields)


