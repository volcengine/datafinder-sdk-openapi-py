# encoding: utf-8
import time
import hashlib
import hmac


def _sha256_hmac(key, data):
    return hmac.new(str.encode(key, 'utf-8'), str.encode(data, 'utf-8'), hashlib.sha256).hexdigest()


def _do_sign(ak, sk, expiration, text):
    sign_key_info = 'ak-v1/%s/%d/%d' % (ak, int(time.time()), expiration)
    sign_key = _sha256_hmac(sk, sign_key_info)
    sign_result = _sha256_hmac(sign_key, text)
    return '%s/%s' % (sign_key_info, sign_result)


def sign(ak, sk, expiration, method, url, params, body):
    text = _canonical_request(method, url, params, body)
    return _do_sign(ak, sk, expiration, text)


def _canonical_request(method, url, params, body):
    canonical_method = _canonical_method(method)
    canonical_url = _canonical_url(url)
    canonical_param = _canonical_param(params)
    canonical_body = _canonical_body(body)
    return '{}\n{}\n{}\n{}'.format(canonical_method, canonical_url, canonical_param, canonical_body)


def _canonical_method(method):
    return "HTTPMethod:" + method


def _canonical_url(url):
    return "CanonicalURI:" + url


def _canonical_param(params):
    res = 'CanonicalQueryString:'
    if not params:
        return res
    kvs = []
    for k, v in params.items():
        kvs.append('{}={}'.format(k, v))
    return res + '&'.join(kvs)


def _canonical_body(body):
    res = "CanonicalBody:"
    if not body:
        return res
    return res + body
